import unittest
from app.services.experiment import summarize_experiment
from app.services.seed import seed_database

class TestExperimentService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()

    def test_five_day_summary(self):
        summary = summarize_experiment("exp-priya-oct", "user-priya-sharma")
        self.assertIsNotNone(summary)
        self.assertEqual(summary["total_days_logged"], 5)
        self.assertGreater(summary["total_extra_hours_recorded"], 0.0)
        self.assertGreater(len(summary["most_common_causes"]), 0)
        self.assertGreater(len(summary["candidate_delegation_tasks"]), 0)
        self.assertIn("Safe Mini-Experiment", summary["safe_next_experiment"])
        self.assertIn("observational reflection patterns", summary["tentative_pattern_disclaimer"])

if __name__ == "__main__":
    unittest.main()
