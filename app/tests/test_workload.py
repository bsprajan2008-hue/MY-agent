import unittest
from app.services.workload import calculate_user_workload, get_team_workload_overview, PRIORITY_WEIGHTS
from app.services.seed import seed_database
from app.database import get_db

class TestWorkloadCalculations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()

    def test_priority_weights(self):
        self.assertEqual(PRIORITY_WEIGHTS["critical"], 1.5)
        self.assertEqual(PRIORITY_WEIGHTS["high"], 1.25)
        self.assertEqual(PRIORITY_WEIGHTS["normal"], 1.0)
        self.assertEqual(PRIORITY_WEIGHTS["deferrable"], 0.75)

    def test_priya_overload_calculation(self):
        # Priya Sharma has heavy lesson prep, grading and voluntary student support
        metrics = calculate_user_workload("user-priya-sharma", "org-oakridge-high")
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics["user_name"], "Priya Sharma")
        self.assertGreater(metrics["capacity_ratio"], 100.0)
        self.assertIn(metrics["capacity_status"], ["moderate_overload", "severe_overload"])
        self.assertGreater(metrics["after_hours_logged"], 0.0)
        self.assertGreater(metrics["voluntary_unplanned_hours"], 0.0)

    def test_marcus_capacity_calculation(self):
        # Marcus Chen has healthy capacity
        metrics = calculate_user_workload("user-marcus-chen", "org-oakridge-high")
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics["user_name"], "Marcus Chen")
        self.assertLess(metrics["capacity_ratio"], 100.0)
        self.assertIn(metrics["capacity_status"], ["available", "balanced"])

    def test_team_workload_overview(self):
        overview = get_team_workload_overview("org-oakridge-high")
        self.assertGreater(overview["total_teachers"], 0)
        self.assertGreaterEqual(overview["overloaded_count"], 1)
        self.assertIsInstance(overview["members"], list)
        self.assertIsInstance(overview["rebalancing_suggestions"], list)
        
        # Verify suggestions never reassign critical tasks
        for sug in overview["rebalancing_suggestions"]:
            self.assertNotEqual(sug["priority"], "critical", "Critical tasks must never be auto-suggested for rebalancing without mutual human planning")

if __name__ == "__main__":
    unittest.main()
