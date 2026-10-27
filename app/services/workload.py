from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from app.database import get_db

PRIORITY_WEIGHTS = {
    "critical": 1.5,
    "high": 1.25,
    "normal": 1.0,
    "deferrable": 0.75
}

def calculate_user_workload(user_id: str, org_id: str) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Fetch user profile
        cursor.execute("""
            SELECT u.*, d.name as department_name 
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = ? AND u.org_id = ?
        """, (user_id, org_id))
        user = cursor.fetchone()
        if not user:
            return {}

        target_hours = float(user.get("weekly_target_hours") or 35.0)
        contracted_periods = int(user.get("contracted_teaching_periods") or 20)
        fixed_commitment_hours = round(contracted_periods * 0.85, 1)

        # 2. Fetch active tasks for this user
        cursor.execute("""
            SELECT * FROM tasks
            WHERE assigned_to_id = ? AND org_id = ? AND status IN ('pending', 'in_progress')
        """, (user_id, org_id))
        active_tasks = cursor.fetchall()

        # 3. Fetch completed tasks in last 30 days to calculate planned vs actual variance
        cursor.execute("""
            SELECT estimated_duration_hours, actual_duration_hours
            FROM tasks
            WHERE assigned_to_id = ? AND org_id = ? AND status = 'completed' AND actual_duration_hours > 0
        """, (user_id, org_id))
        completed_tasks = cursor.fetchall()

        # 4. Fetch actual time logs recorded in the current rolling 7 days
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT * FROM time_logs
            WHERE user_id = ? AND org_id = ? AND log_date >= ?
        """, (user_id, org_id, seven_days_ago))
        recent_logs = cursor.fetchall()

    # Calculate actual logged hours this week
    actual_logged_hours = sum(log["duration_hours"] for log in recent_logs)
    after_hours_logged = sum(log["duration_hours"] for log in recent_logs if log["is_after_hours"] == 1)

    # Calculate task totals and weighted burden
    total_assigned_estimated = 0.0
    weighted_task_burden = 0.0
    critical_hours = 0.0
    high_hours = 0.0
    normal_hours = 0.0
    deferrable_hours = 0.0
    voluntary_unplanned_hours = 0.0
    unclear_ownership_count = 0
    tasks_missing_actuals_count = 0

    priority_counts = {"critical": 0, "high": 0, "normal": 0, "deferrable": 0}
    category_hours = {}

    for t in active_tasks:
        est = float(t["estimated_duration_hours"] or 1.0)
        prio = t["priority"]
        weight = PRIORITY_WEIGHTS.get(prio, 1.0)
        
        total_assigned_estimated += est
        weighted_task_burden += (est * weight)
        priority_counts[prio] = priority_counts.get(prio, 0) + 1

        if prio == "critical":
            critical_hours += est
        elif prio == "high":
            high_hours += est
        elif prio == "normal":
            normal_hours += est
        elif prio == "deferrable":
            deferrable_hours += est

        cat = t["category"]
        category_hours[cat] = category_hours.get(cat, 0.0) + est

        if t["assignment_type"] in ("voluntarily_taken", "unclear_owner", "emergency_work"):
            voluntary_unplanned_hours += est

        if t["assignment_type"] == "unclear_owner":
            unclear_ownership_count += 1

        if float(t["actual_duration_hours"] or 0) == 0:
            tasks_missing_actuals_count += 1

    # Planned vs Actual Variance Ratio
    if completed_tasks:
        total_est_comp = sum(float(c["estimated_duration_hours"]) for c in completed_tasks)
        total_act_comp = sum(float(c["actual_duration_hours"]) for c in completed_tasks)
        variance_ratio = round(total_act_comp / total_est_comp, 2) if total_est_comp > 0 else 1.0
    else:
        variance_ratio = 1.0

    # Total estimated weekly load: Fixed commitments + Weighted Assigned Tasks + (0.3 * Unplanned Volatility)
    total_projected_load = round(fixed_commitment_hours + weighted_task_burden + (0.3 * voluntary_unplanned_hours), 1)
    
    # Capacity Percentage
    capacity_ratio = round((total_projected_load / target_hours) * 100, 1)

    if capacity_ratio < 85.0:
        capacity_status = "available"  # Healthy, capacity to help
        status_label = "Available Capacity"
        color = "emerald"
    elif capacity_ratio <= 105.0:
        capacity_status = "balanced"  # Optimal
        status_label = "Balanced & Sustainable"
        color = "blue"
    elif capacity_ratio <= 125.0:
        capacity_status = "moderate_overload"  # Action advised
        status_label = "Moderate Overload"
        color = "amber"
    else:
        capacity_status = "severe_overload"  # Action required
        status_label = "Severe Overload Risk"
        color = "rose"

    # Explainable calculation breakdown
    explanation_factors = [
        {
            "factor": "Fixed Commitments",
            "hours": fixed_commitment_hours,
            "description": f"{contracted_periods} contracted periods/clinical shifts (~0.85h each)"
        },
        {
            "factor": "Direct Assigned Tasks",
            "hours": round(total_assigned_estimated, 1),
            "description": f"{len(active_tasks)} active tasks in current queue"
        },
        {
            "factor": "Urgency & Complexity Multiplier",
            "hours": round(weighted_task_burden - total_assigned_estimated, 1),
            "description": f"Weight additions ({priority_counts['critical']} critical, {priority_counts['high']} high)"
        },
        {
            "factor": "Unplanned & Voluntary Work",
            "hours": round(voluntary_unplanned_hours, 1),
            "description": f"Tasks absorbed without formal assignment or with unclear owner"
        }
    ]

    missing_data_notes = []
    if tasks_missing_actuals_count > 0:
        missing_data_notes.append(f"{tasks_missing_actuals_count} active tasks currently lack logged actual duration.")
    if len(recent_logs) == 0:
        missing_data_notes.append("No time logs recorded in the past 7 days; calculation relies on estimated task hours.")

    return {
        "user_id": user_id,
        "user_name": user["name"],
        "user_email": user["email"],
        "role": user["role"],
        "department_name": user.get("department_name") or "General",
        "target_hours": target_hours,
        "fixed_commitment_hours": fixed_commitment_hours,
        "contracted_teaching_periods": contracted_periods,
        "active_task_count": len(active_tasks),
        "total_assigned_estimated": round(total_assigned_estimated, 1),
        "weighted_task_burden": round(weighted_task_burden, 1),
        "total_projected_load": total_projected_load,
        "capacity_ratio": capacity_ratio,
        "capacity_status": capacity_status,
        "status_label": status_label,
        "color": color,
        "actual_logged_hours_this_week": round(actual_logged_hours, 1),
        "after_hours_logged": round(after_hours_logged, 1),
        "personal_time_lost_hours": round(max(0.0, actual_logged_hours - target_hours) + after_hours_logged, 1),
        "voluntary_unplanned_hours": round(voluntary_unplanned_hours, 1),
        "unclear_ownership_count": unclear_ownership_count,
        "variance_ratio": variance_ratio,
        "priority_breakdown": {
            "critical_hours": round(critical_hours, 1),
            "high_hours": round(high_hours, 1),
            "normal_hours": round(normal_hours, 1),
            "deferrable_hours": round(deferrable_hours, 1),
            "counts": priority_counts
        },
        "category_hours": category_hours,
        "explanation_factors": explanation_factors,
        "missing_data_notes": missing_data_notes
    }

def get_team_workload_overview(org_id: str) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE org_id = ? AND role = 'teacher'", (org_id,))
        teachers = cursor.fetchall()
        
        cursor.execute("SELECT * FROM tasks WHERE org_id = ? AND status IN ('pending', 'in_progress')", (org_id,))
        all_active_tasks = cursor.fetchall()

    members = []
    overloaded_count = 0
    balanced_count = 0
    available_count = 0

    for t in teachers:
        metrics = calculate_user_workload(t["id"], org_id)
        if metrics:
            members.append(metrics)
            if metrics["capacity_status"] in ("moderate_overload", "severe_overload"):
                overloaded_count += 1
            elif metrics["capacity_status"] == "balanced":
                balanced_count += 1
            else:
                available_count += 1

    # Sort members by capacity ratio descending (most loaded first)
    members.sort(key=lambda x: x["capacity_ratio"], reverse=True)

    # Rebalancing Opportunities Finder
    rebalancing_suggestions = []
    overloaded_members = [m for m in members if m["capacity_status"] in ("moderate_overload", "severe_overload")]
    available_members = [m for m in members if m["capacity_status"] in ("available", "balanced") and m["capacity_ratio"] < 95.0]

    for overloaded in overloaded_members:
        # Find tasks that are deferrable or normal, non-critical
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM tasks 
                WHERE assigned_to_id = ? AND org_id = ? 
                AND priority IN ('deferrable', 'normal') 
                AND status IN ('pending', 'in_progress')
                ORDER BY priority ASC, estimated_duration_hours DESC
            """, (overloaded["user_id"], org_id))
            candidates = cursor.fetchall()

        for cand in candidates:
            # Match with an available colleague, preferably in the same department
            best_candidate = None
            for avail in available_members:
                # Calculate projected capacity if this task is accepted
                added_load = float(cand["estimated_duration_hours"] or 1.0)
                new_projected = avail["total_projected_load"] + added_load
                new_ratio = (new_projected / avail["target_hours"]) * 100
                if new_ratio <= 100.0:
                    best_candidate = avail
                    break

            if best_candidate:
                rebalancing_suggestions.append({
                    "task_id": cand["id"],
                    "task_title": cand["title"],
                    "category": cand["category"],
                    "priority": cand["priority"],
                    "estimated_hours": cand["estimated_duration_hours"],
                    "from_user_id": overloaded["user_id"],
                    "from_user_name": overloaded["user_name"],
                    "to_user_id": best_candidate["user_id"],
                    "to_user_name": best_candidate["user_name"],
                    "reason": f"Reduces {overloaded['user_name']}'s {overloaded['capacity_ratio']}% load by {cand['estimated_duration_hours']}h while keeping {best_candidate['user_name']} within healthy capacity ({round(best_candidate['capacity_ratio'], 1)}%). Requires manager human approval."
                })

    return {
        "total_teachers": len(members),
        "overloaded_count": overloaded_count,
        "balanced_count": balanced_count,
        "available_count": available_count,
        "members": members,
        "rebalancing_suggestions": rebalancing_suggestions
    }
