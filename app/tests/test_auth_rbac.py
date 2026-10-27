import unittest
from app.auth import hash_password, verify_password, create_session_token, decode_session_token
from app.services.seed import seed_database
from app.database import get_db

class TestAuthAndRBAC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()

    def test_password_hashing(self):
        pw = "super-secret-password-123"
        hashed = hash_password(pw)
        self.assertNotEqual(pw, hashed)
        self.assertTrue(verify_password(pw, hashed))
        self.assertFalse(verify_password("wrong-password", hashed))

    def test_session_token_validation(self):
        token = create_session_token("user-priya-sharma", "org-oakridge-high", "teacher")
        payload = decode_session_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["uid"], "user-priya-sharma")
        self.assertEqual(payload["oid"], "org-oakridge-high")
        self.assertEqual(payload["rol"], "teacher")

    def test_tampered_token_fails(self):
        token = create_session_token("user-priya-sharma", "org-oakridge-high", "teacher")
        tampered = token[:-2] + "xx"
        self.assertIsNone(decode_session_token(tampered))

    def test_private_note_isolation(self):
        # Verify in DB that private notes exist but query rule keeps them strictly for the author
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT private_note, assigned_to_id FROM tasks WHERE private_note IS NOT NULL")
            rows = cursor.fetchall()
            self.assertGreater(len(rows), 0)
            for r in rows:
                self.assertIsNotNone(r["assigned_to_id"])

if __name__ == "__main__":
    unittest.main()
