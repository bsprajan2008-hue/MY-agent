import os
import json
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
import io
import csv

from app.config import PORT, HOST, SECRET_KEY, GEMINI_API_KEY
from app.database import get_db, init_db
from app.models import (
    LoginRequest, SwitchUserRequest, UserCreate, TaskCreate, TaskUpdate,
    TimeLogCreate, WorkloadRequestCreate, WorkloadRequestRespond,
    ReassignTaskRequest, ExperimentEntryCreate, AIPromptRequest, OrgSettingsUpdate
)
from app.auth import (
    verify_password, create_session_token, get_current_user,
    require_role, hash_password
)
from app.services.workload import calculate_user_workload, get_team_workload_overview
from app.services.experiment import summarize_experiment
from app.services.ai_insights import get_ai_workload_insights
from app.services.seed import seed_database

app = FastAPI(
    title="FAIRSHIFT API",
    description="Fair Workload and Well-being Platform for Schools and Employee-Intensive Organisations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# AUTHENTICATION & DEMO SWITCHER ROUTES
# -------------------------------------------------------------------
@app.post("/api/auth/login")
def login(req: LoginRequest, response: Response):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (req.email.strip().lower(),))
        user = cursor.fetchone()
        
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    token = create_session_token(user["id"], user["org_id"], user["role"])
    response.set_cookie(
        key="fairshift_session",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )
    user_data = dict(user)
    del user_data["password_hash"]
    return {"status": "success", "token": token, "user": user_data}

@app.post("/api/auth/logout")
def logout(response: Response):
    response.delete_cookie("fairshift_session")
    return {"status": "success", "message": "Logged out successfully"}

@app.get("/api/auth/me")
def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    user_data = dict(user)
    if "password_hash" in user_data:
        del user_data["password_hash"]
    return user_data

@app.get("/api/auth/demo-users")
def get_demo_users():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.role, u.avatar_url, o.name as org_name, o.industry, d.name as department_name
            FROM users u
            JOIN organisations o ON u.org_id = o.id
            LEFT JOIN departments d ON u.department_id = d.id
            ORDER BY o.industry ASC, u.role DESC
        """)
        users = cursor.fetchall()
    return users

@app.post("/api/auth/switch-demo")
def switch_demo_user(req: SwitchUserRequest, response: Response):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.*, o.name as org_name, o.industry as org_industry, d.name as department_name
            FROM users u
            JOIN organisations o ON u.org_id = o.id
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = ?
        """, (req.user_id,))
        user = cursor.fetchone()
        
    if not user:
        raise HTTPException(status_code=404, detail="Demo user not found.")
        
    token = create_session_token(user["id"], user["org_id"], user["role"])
    response.set_cookie(
        key="fairshift_session",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )
    user_data = dict(user)
    del user_data["password_hash"]
    return {"status": "success", "token": token, "user": user_data}

# -------------------------------------------------------------------
# TASKS MANAGEMENT ROUTES
# -------------------------------------------------------------------
@app.get("/api/tasks")
def list_tasks(
    status_filter: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    scope: str = "my",  # "my" or "team"
    user: Dict[str, Any] = Depends(get_current_user)
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT t.*, 
                   u_assignee.name as assigned_to_name,
                   u_creator.name as assigned_by_name,
                   d.name as department_name
            FROM tasks t
            LEFT JOIN users u_assignee ON t.assigned_to_id = u_assignee.id
            LEFT JOIN users u_creator ON t.assigned_by_id = u_creator.id
            LEFT JOIN departments d ON t.department_id = d.id
            WHERE t.org_id = ?
        """
        params = [user["org_id"]]

        if scope == "my" or user["role"] == "teacher":
            query += " AND t.assigned_to_id = ?"
            params.append(user["id"])
        
        if status_filter:
            query += " AND t.status = ?"
            params.append(status_filter)
        if category:
            query += " AND t.category = ?"
            params.append(category)
        if priority:
            query += " AND t.priority = ?"
            params.append(priority)

        query += " ORDER BY CASE t.priority WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'normal' THEN 3 ELSE 4 END, t.due_date ASC"
        cursor.execute(query, params)
        tasks = cursor.fetchall()

    # Privacy Protection Rule: hide private notes if requester is not the task's assignee
    sanitized = []
    for t in tasks:
        t_dict = dict(t)
        if t_dict.get("assigned_to_id") != user["id"]:
            t_dict["private_note"] = None
        sanitized.append(t_dict)

    return sanitized

@app.post("/api/tasks")
def create_task(req: TaskCreate, user: Dict[str, Any] = Depends(get_current_user)):
    task_id = f"task-{uuid.uuid4().hex[:10]}"
    assigned_to = req.assigned_to_id if req.assigned_to_id else user["id"]

    # If teacher is creating and assigns to another colleague without manager role, verify permission
    if user["role"] == "teacher" and assigned_to != user["id"]:
        raise HTTPException(status_code=403, detail="Teachers can only self-assign or record voluntary tasks. Manager approval required to assign tasks to other staff.")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (
                id, org_id, department_id, title, description, category,
                assigned_to_id, assigned_by_id, collaborators,
                estimated_duration_hours, actual_duration_hours, due_date,
                priority, status, is_recurring, assignment_type,
                completed_within_scheduled_hours, extra_work_reason, private_note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_id, user["org_id"], user.get("department_id"), req.title, req.description, req.category,
            assigned_to, user["id"], json.dumps(req.collaborators or []),
            req.estimated_duration_hours, req.actual_duration_hours or 0.0, req.due_date,
            req.priority, req.status, 1 if req.is_recurring else 0, req.assignment_type,
            1 if req.completed_within_scheduled_hours else 0, req.extra_work_reason or "none", req.private_note
        ))

        # Record audit event
        cursor.execute("""
            INSERT INTO audit_events (id, org_id, actor_id, actor_role, action, target_type, target_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), user["org_id"], user["id"], user["role"], "create_task", "task", task_id, json.dumps({"title": req.title, "priority": req.priority})))

    return {"status": "success", "task_id": task_id, "message": "Task recorded successfully"}

@app.patch("/api/tasks/{task_id}")
def update_task(task_id: str, req: TaskUpdate, user: Dict[str, Any] = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ? AND org_id = ?", (task_id, user["org_id"]))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Task not found.")

        # Ownership / Role check
        if user["role"] == "teacher" and existing["assigned_to_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="You can only update tasks assigned to yourself.")

        updates = []
        params = []
        for field, val in req.model_dump(exclude_unset=True).items():
            if field == "collaborators" and val is not None:
                updates.append(f"{field} = ?")
                params.append(json.dumps(val))
            elif field in ("is_recurring", "completed_within_scheduled_hours") and val is not None:
                updates.append(f"{field} = ?")
                params.append(1 if val else 0)
            elif field == "private_note":
                # Only the assignee may update their private note
                if existing["assigned_to_id"] == user["id"]:
                    updates.append("private_note = ?")
                    params.append(val)
            elif val is not None:
                updates.append(f"{field} = ?")
                params.append(val)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.extend([task_id, user["org_id"]])
            cursor.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND org_id = ?", params)

    return {"status": "success", "message": "Task updated successfully"}

# -------------------------------------------------------------------
# TIME LOGGING ROUTES
# -------------------------------------------------------------------
@app.get("/api/timelogs")
def get_timelogs(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.*, t.title as task_title, t.category as task_category, t.priority as task_priority
            FROM time_logs l
            LEFT JOIN tasks t ON l.task_id = t.id
            WHERE l.user_id = ? AND l.org_id = ?
            ORDER BY l.log_date DESC, l.created_at DESC
        """, (user["id"], user["org_id"]))
        logs = cursor.fetchall()
    return logs

@app.post("/api/timelogs")
def create_timelog(req: TimeLogCreate, user: Dict[str, Any] = Depends(get_current_user)):
    log_id = f"log-{uuid.uuid4().hex[:10]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO time_logs (id, org_id, task_id, user_id, log_date, duration_hours, is_after_hours, reason, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            log_id, user["org_id"], req.task_id, user["id"], req.log_date,
            req.duration_hours, 1 if req.is_after_hours else 0, req.reason, req.notes
        ))
        
        # If linked to a task, update the task's actual_duration_hours accumulator
        if req.task_id:
            cursor.execute("""
                UPDATE tasks 
                SET actual_duration_hours = actual_duration_hours + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND org_id = ?
            """, (req.duration_hours, req.task_id, user["org_id"]))

    return {"status": "success", "log_id": log_id, "message": "Time log recorded"}

# -------------------------------------------------------------------
# WORKLOAD ANALYTICS & REBALANCING
# -------------------------------------------------------------------
@app.get("/api/workload/personal")
def get_personal_workload(user: Dict[str, Any] = Depends(get_current_user)):
    metrics = calculate_user_workload(user["id"], user["org_id"])
    return metrics

@app.get("/api/workload/team")
def get_team_workload(user: Dict[str, Any] = Depends(require_role("manager", "coordinator"))):
    overview = get_team_workload_overview(user["org_id"])
    return overview

@app.post("/api/workload/reassign")
def reassign_task(req: ReassignTaskRequest, user: Dict[str, Any] = Depends(require_role("manager", "coordinator"))):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ? AND org_id = ?", (req.task_id, user["org_id"]))
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")

        cursor.execute("SELECT * FROM users WHERE id = ? AND org_id = ?", (req.new_user_id, user["org_id"]))
        new_user = cursor.fetchone()
        if not new_user:
            raise HTTPException(status_code=404, detail="Target assignee not found.")

        prev_user_id = task["assigned_to_id"]

        # Never auto-reassign critical student safety tasks without explicit warning check
        if task["priority"] == "critical" and "critical_confirmed" not in req.reason.lower():
            # Allowed if reasoned, but require meaningful documented justification
            if len(req.reason) < 10:
                raise HTTPException(status_code=400, detail="Reassigning a critical priority task requires a comprehensive documented justification.")

        # Update task assignee
        cursor.execute("""
            UPDATE tasks 
            SET assigned_to_id = ?,
                assignment_type = 'formally_assigned',
                status = 'pending',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND org_id = ?
        """, (req.new_user_id, req.task_id, user["org_id"]))

        # Record reassignment history
        rec_id = f"reassign-{uuid.uuid4().hex[:10]}"
        cursor.execute("""
            INSERT INTO reassignment_records (id, org_id, task_id, previous_user_id, new_user_id, reassigned_by_id, reason, approved_by_human)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """, (rec_id, user["org_id"], req.task_id, prev_user_id, req.new_user_id, user["id"], req.reason))

        # Record Audit Event
        cursor.execute("""
            INSERT INTO audit_events (id, org_id, actor_id, actor_role, action, target_type, target_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), user["org_id"], user["id"], user["role"], "reassign_task", "task", req.task_id, json.dumps({
            "task_title": task["title"],
            "from_user": prev_user_id,
            "to_user": req.new_user_id,
            "reason": req.reason
        })))

    return {"status": "success", "message": f"Task '{task['title']}' successfully reassigned to {new_user['name']} with documented rationale."}

# -------------------------------------------------------------------
# RESPECTFUL REQUEST & GRIEVANCE CHANNEL (MVP FEATURE 3 & 5)
# -------------------------------------------------------------------
@app.get("/api/requests")
def list_requests(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        if user["role"] in ("manager", "coordinator"):
            cursor.execute("""
                SELECT r.*, 
                       u_author.name as author_name, u_author.email as author_email,
                       ta.title as task_a_title, ta.priority as task_a_priority,
                       tb.title as task_b_title, tb.priority as task_b_priority
                FROM workload_requests r
                JOIN users u_author ON r.user_id = u_author.id
                LEFT JOIN tasks ta ON r.task_a_id = ta.id
                LEFT JOIN tasks tb ON r.task_b_id = tb.id
                WHERE r.org_id = ?
                ORDER BY r.created_at DESC
            """, (user["org_id"],))
        else:
            cursor.execute("""
                SELECT r.*, 
                       u_author.name as author_name,
                       ta.title as task_a_title, ta.priority as task_a_priority,
                       tb.title as task_b_title, tb.priority as task_b_priority
                FROM workload_requests r
                JOIN users u_author ON r.user_id = u_author.id
                LEFT JOIN tasks ta ON r.task_a_id = ta.id
                LEFT JOIN tasks tb ON r.task_b_id = tb.id
                WHERE r.user_id = ? AND r.org_id = ?
                ORDER BY r.created_at DESC
            """, (user["id"], user["org_id"]))
        requests_list = cursor.fetchall()
    return requests_list

@app.post("/api/requests")
def submit_request(req: WorkloadRequestCreate, user: Dict[str, Any] = Depends(get_current_user)):
    req_id = f"req-{uuid.uuid4().hex[:10]}"
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Locate designated manager or principal for the org
        manager_id = req.assigned_to_manager_id
        if not manager_id:
            cursor.execute("SELECT id FROM users WHERE org_id = ? AND role = 'manager' LIMIT 1", (user["org_id"],))
            mgr = cursor.fetchone()
            manager_id = mgr["id"] if mgr else None

        cursor.execute("""
            INSERT INTO workload_requests (
                id, org_id, user_id, assigned_to_manager_id, request_type,
                task_a_id, task_b_id, available_time_hours, message,
                access_scope, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'submitted')
        """, (
            req_id, user["org_id"], user["id"], manager_id, req.request_type,
            req.task_a_id, req.task_b_id, req.available_time_hours, req.message,
            req.access_scope
        ))

        cursor.execute("""
            INSERT INTO audit_events (id, org_id, actor_id, actor_role, action, target_type, target_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), user["org_id"], user["id"], user["role"], "submit_request", "workload_request", req_id, json.dumps({
            "type": req.request_type, "access_scope": req.access_scope
        })))

    return {"status": "success", "request_id": req_id, "message": "Request submitted respectfully. Your manager has been notified."}

@app.patch("/api/requests/{request_id}/respond")
def respond_to_request(request_id: str, req: WorkloadRequestRespond, user: Dict[str, Any] = Depends(require_role("manager", "coordinator"))):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workload_requests WHERE id = ? AND org_id = ?", (request_id, user["org_id"]))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Request not found.")

        cursor.execute("""
            UPDATE workload_requests
            SET status = ?,
                manager_response = ?,
                resolved_at = CURRENT_TIMESTAMP
            WHERE id = ? AND org_id = ?
        """, (req.status, req.manager_response, request_id, user["org_id"]))

        cursor.execute("""
            INSERT INTO audit_events (id, org_id, actor_id, actor_role, action, target_type, target_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), user["org_id"], user["id"], user["role"], "respond_request", "workload_request", request_id, json.dumps({
            "status": req.status, "author_id": existing["user_id"]
        })))

    return {"status": "success", "message": "Response recorded and shared with employee."}

# -------------------------------------------------------------------
# SAFE FIVE-DAY WORKLOAD EXPERIMENT (MVP FEATURE 4)
# -------------------------------------------------------------------
@app.get("/api/experiments/current")
def get_current_experiment(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM experiments 
            WHERE user_id = ? AND org_id = ? 
            ORDER BY created_at DESC LIMIT 1
        """, (user["id"], user["org_id"]))
        exp = cursor.fetchone()
        
        if not exp:
            return None

        cursor.execute("""
            SELECT * FROM experiment_entries
            WHERE experiment_id = ? AND user_id = ?
            ORDER BY day_number ASC, created_at ASC
        """, (exp["id"], user["id"]))
        entries = cursor.fetchall()

    summary = summarize_experiment(exp["id"], user["id"])
    return {
        "experiment": exp,
        "entries": entries,
        "summary": summary
    }

@app.post("/api/experiments")
def start_experiment(user: Dict[str, Any] = Depends(get_current_user)):
    exp_id = f"exp-{uuid.uuid4().hex[:10]}"
    start_date = datetime.now().strftime("%Y-%m-%d")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO experiments (id, org_id, user_id, start_date, status)
            VALUES (?, ?, ?, ?, 'active')
        """, (exp_id, user["org_id"], user["id"], start_date))
    return {"status": "success", "experiment_id": exp_id, "message": "5-Day Workload Experiment commenced."}

@app.post("/api/experiments/{experiment_id}/entries")
def add_experiment_entry(experiment_id: str, req: ExperimentEntryCreate, user: Dict[str, Any] = Depends(get_current_user)):
    entry_id = f"ee-{uuid.uuid4().hex[:10]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO experiment_entries (
                id, experiment_id, user_id, day_number, task_title, category,
                hours_spent, extra_work_cause, perceived_consequence, actual_outcome, candidate_action
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry_id, experiment_id, user["id"], req.day_number, req.task_title, req.category,
            req.hours_spent, req.extra_work_cause, req.perceived_consequence, req.actual_outcome, req.candidate_action
        ))
        
        # Check if 5 days logged to mark completed
        cursor.execute("SELECT COUNT(DISTINCT day_number) as num_days FROM experiment_entries WHERE experiment_id = ?", (experiment_id,))
        cnt = cursor.fetchone()["num_days"]
        if cnt >= 5:
            cursor.execute("UPDATE experiments SET status = 'completed', end_date = ? WHERE id = ?", (datetime.now().strftime("%Y-%m-%d"), experiment_id))

    return {"status": "success", "entry_id": entry_id, "message": "Day record added successfully."}

@app.delete("/api/experiments/{experiment_id}")
def delete_experiment(experiment_id: str, user: Dict[str, Any] = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM experiments WHERE id = ? AND user_id = ?", (experiment_id, user["id"]))
    return {"status": "success", "message": "Experiment and entries permanently deleted."}

# -------------------------------------------------------------------
# AI WORKLOAD INSIGHTS (MVP FEATURE 6)
# -------------------------------------------------------------------
@app.post("/api/ai/insights")
def get_insights(req: AIPromptRequest, user: Dict[str, Any] = Depends(get_current_user)):
    # Role check: only managers can request target_user_id for others
    target_id = user["id"]
    if req.target_user_id and req.target_user_id != user["id"]:
        if user["role"] not in ("manager", "coordinator"):
            raise HTTPException(status_code=403, detail="Only managers can view team member analytics.")
        target_id = req.target_user_id

    insights = get_ai_workload_insights(
        user_id=user["id"],
        org_id=user["org_id"],
        mode=req.mode,
        task_id=req.task_id,
        target_user_id=target_id,
        include_private_notes=req.include_private_notes,
        user_context=req.user_context
    )
    return insights

# -------------------------------------------------------------------
# SETTINGS, DATA EXPORT & PRIVACY
# -------------------------------------------------------------------
@app.get("/api/settings")
def get_settings(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM organisation_settings WHERE org_id = ?", (user["org_id"],))
        settings = cursor.fetchone()
    return settings or {
        "standard_weekly_hours": 35.0,
        "default_language": "en",
        "enable_anonymous_feedback_threshold": 3
    }

@app.patch("/api/settings")
def update_settings(req: OrgSettingsUpdate, user: Dict[str, Any] = Depends(require_role("coordinator", "manager"))):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE organisation_settings
            SET standard_weekly_hours = COALESCE(?, standard_weekly_hours),
                enable_anonymous_feedback_threshold = COALESCE(?, enable_anonymous_feedback_threshold),
                default_language = COALESCE(?, default_language),
                updated_at = CURRENT_TIMESTAMP
            WHERE org_id = ?
        """, (req.standard_weekly_hours, req.enable_anonymous_feedback_threshold, req.default_language, user["org_id"]))
    return {"status": "success", "message": "Settings updated"}

@app.get("/api/export/workload-csv")
def export_csv(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.title, t.category, t.priority, t.status, t.estimated_duration_hours,
                   t.actual_duration_hours, t.due_date, t.assignment_type, t.extra_work_reason
            FROM tasks t
            WHERE t.assigned_to_id = ? AND t.org_id = ?
            ORDER BY t.due_date ASC
        """, (user["id"], user["org_id"]))
        rows = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Task Title", "Category", "Priority", "Status", "Estimated Hours",
        "Actual Hours", "Due Date", "Assignment Type", "Extra Work Reason"
    ])
    for r in rows:
        writer.writerow([
            r["title"], r["category"], r["priority"], r["status"],
            r["estimated_duration_hours"], r["actual_duration_hours"],
            r["due_date"], r["assignment_type"], r["extra_work_reason"]
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=fairshift-workload-{user['name'].replace(' ', '_')}.csv"}
    )

@app.post("/api/admin/reset-seed")
def reset_seed(user: Dict[str, Any] = Depends(require_role("manager", "coordinator"))):
    seed_database()
    return {"status": "success", "message": "Demo database successfully re-seeded to initial state."}

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(index_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
