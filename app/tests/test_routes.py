import unittest
from fastapi import HTTPException
from app.services.seed import seed_database
from app.database import get_db
from app.models import (
    TaskCreate, TaskUpdate, TimeLogCreate, WorkloadRequestCreate,
    WorkloadRequestRespond, ReassignTaskRequest, ExperimentEntryCreate,
    AIPromptRequest
)
from app.main import (
    list_tasks, create_task, update_task, get_timelogs, create_timelog,
    get_personal_workload, get_team_workload, reassign_task,
    list_requests, submit_request, respond_to_request,
    get_current_experiment, add_experiment_entry, get_insights
)

class TestRouteHandlers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = 'user-priya-sharma'")
            cls.teacher_user = cursor.fetchone()
            cursor.execute("SELECT * FROM users WHERE id = 'user-sarah-jenkins'")
            cls.manager_user = cursor.fetchone()
            cursor.execute("SELECT * FROM users WHERE id = 'user-marcus-chen'")
            cls.colleague_user = cursor.fetchone()

    def test_list_tasks_and_private_notes_protection(self):
        # Teacher viewing their own tasks
        my_tasks = list_tasks(scope="my", user=self.teacher_user)
        self.assertGreater(len(my_tasks), 0)
        # Should see their own private notes if present
        has_private = any(t.get("private_note") is not None for t in my_tasks)
        self.assertTrue(has_private, "Teacher should see their own private notes")

        # Manager viewing all tasks
        team_tasks = list_tasks(scope="team", user=self.manager_user)
        # Manager must NEVER see Priya's private notes
        priya_tasks_seen_by_manager = [t for t in team_tasks if t["assigned_to_id"] == "user-priya-sharma"]
        for pt in priya_tasks_seen_by_manager:
            self.assertIsNone(pt.get("private_note"), "Manager must not see private notes of another employee")

    def test_create_and_update_task(self):
        new_task = TaskCreate(
            title="Design Tiered Reading Rubric",
            category="lesson preparation",
            estimated_duration_hours=3.0,
            due_date="2026-11-05",
            priority="normal",
            assignment_type="voluntarily_taken",
            extra_work_reason="student_needs",
            private_note="Testing self-regulated reading scaffolding."
        )
        res = create_task(new_task, user=self.teacher_user)
        self.assertEqual(res["status"], "success")
        task_id = res["task_id"]

        # Update task status to completed
        update_res = update_task(task_id, TaskUpdate(status="completed", actual_duration_hours=2.5), user=self.teacher_user)
        self.assertEqual(update_res["status"], "success")

    def test_log_time_updates_task_actuals(self):
        tl = TimeLogCreate(
            task_id="task-priya-1",
            log_date="2026-10-27",
            duration_hours=2.0,
            is_after_hours=True,
            reason="student_needs",
            notes="Late-night essay margin comments."
        )
        res = create_timelog(tl, user=self.teacher_user)
        self.assertEqual(res["status"], "success")

    def test_submit_and_respond_workload_request(self):
        req_input = WorkloadRequestCreate(
            request_type="clarification",
            task_a_id="task-priya-1",
            task_b_id="task-priya-4",
            available_time_hours=4.0,
            message="I have essay grading and textbook inventory competing for 4h. Which should take priority?",
            access_scope="manager_only"
        )
        res = submit_request(req_input, user=self.teacher_user)
        self.assertEqual(res["status"], "success")
        req_id = res["request_id"]

        # Manager responds
        resp_input = WorkloadRequestRespond(
            status="resolved",
            manager_response="Prioritise essay grading; textbook inventory is deferred to term break."
        )
        resp_res = respond_to_request(req_id, resp_input, user=self.manager_user)
        self.assertEqual(resp_res["status"], "success")

    def test_manager_reassignment_with_audit(self):
        reassign_input = ReassignTaskRequest(
            task_id="task-priya-4",
            new_user_id="user-marcus-chen",
            reason="Rebalancing non-urgent admin inventory to protect teacher exam planning block."
        )
        res = reassign_task(reassign_input, user=self.manager_user)
        self.assertEqual(res["status"], "success")

        # Verify teacher role cannot reassign tasks
        with self.assertRaises(HTTPException):
            # require_role raises 403 for teacher
            from app.auth import require_role
            role_checker = require_role("manager", "coordinator")
            role_checker(self.teacher_user)

    def test_ai_advisor_dispatch(self):
        res = get_insights(
            AIPromptRequest(mode="summarize_workload"),
            user=self.teacher_user
        )
        self.assertIn("Priya Sharma", res["title"])
        self.assertIn("disclaimer", res)

if __name__ == "__main__":
    unittest.main()
