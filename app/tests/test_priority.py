import unittest
from app.services.seed import seed_database
from app.database import get_db

class TestPriorityWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()

    def test_student_critical_priority_rules(self):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE priority = 'critical'")
            critical_tasks = cursor.fetchall()
            
            self.assertGreater(len(critical_tasks), 0)
            for ct in critical_tasks:
                # Critical tasks must not be deferrable category or default auto-dismissed
                self.assertIn(ct["category"], ["teaching", "assessment", "student support", "administration"])
                self.assertIn(ct["status"], ["pending", "in_progress", "completed"])

    def test_workload_request_conflict_structure(self):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM workload_requests WHERE request_type = 'clarification'")
            req = cursor.fetchone()
            
            self.assertIsNotNone(req)
            self.assertIn("competing for", req["message"])
            self.assertIsNotNone(req["task_a_id"])
            self.assertIsNotNone(req["task_b_id"])

if __name__ == "__main__":
    unittest.main()
