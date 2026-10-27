import unittest
from app.services.ai_insights import get_ai_workload_insights
from app.services.seed import seed_database

class TestAIFallback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()

    def test_deterministic_insights_without_api_key(self):
        insights = get_ai_workload_insights(
            user_id="user-priya-sharma",
            org_id="org-oakridge-high",
            mode="summarize_workload"
        )
        self.assertIsNotNone(insights)
        self.assertEqual(insights["mode"], "summarize_workload")
        self.assertIn("Priya Sharma", insights["title"])
        self.assertIsInstance(insights["bullet_points"], list)
        self.assertIn("evidence", insights)
        self.assertIn("disclaimer", insights)
        self.assertIn("human review", insights["disclaimer"].lower())

    def test_draft_respectful_request_fallback(self):
        insights = get_ai_workload_insights(
            user_id="user-priya-sharma",
            org_id="org-oakridge-high",
            mode="draft_request"
        )
        self.assertIsNotNone(insights)
        self.assertEqual(insights["mode"], "draft_request")
        self.assertIn("Dear Manager", insights["text"])
        self.assertIn("student", insights["text"].lower())

    def test_suggest_questions_fallback(self):
        insights = get_ai_workload_insights(
            user_id="user-priya-sharma",
            org_id="org-oakridge-high",
            mode="suggest_questions"
        )
        self.assertIsNotNone(insights)
        self.assertGreater(len(insights["bullet_points"]), 0)

if __name__ == "__main__":
    unittest.main()
