import unittest
from fastapi.testclient import TestClient
from main import app

class TestFullAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.test_username = "testuser"
        self.test_email = "test@example.com"
        self.test_password = "password123"

    def test_01_check_username_available(self):
        response = self.client.get(f"/api/v1/users/check-username/{self.test_username}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_available"])

    def test_02_register_user(self):
        payload = {
            "username": self.test_username,
            "email": self.test_email,
            "password": self.test_password,
            "full_name": "Test User"
        }
        response = self.client.post("/api/v1/auth/register", json=payload)
        self.assertIn(response.status_code, [201, 400])  # 201 or 400 if already exists

    def test_03_login_user(self):
        payload = {
            "username": self.test_username,
            "password": self.test_password
        }
        response = self.client.post("/api/v1/auth/login", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        token = data["access_token"]

        # Test GET /me
        headers = {"Authorization": f"Bearer {token}"}
        me_resp = self.client.get("/api/v1/users/me", headers=headers)
        self.assertEqual(me_resp.status_code, 200)
        self.assertEqual(me_resp.json()["username"], self.test_username)

    def test_04_get_all_users_pagination(self):
        response = self.client.get("/api/v1/users?skip=0&limit=5")
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertIsInstance(users, list)

    def test_05_script_generation(self):
        payload = {
            "target_language": "python",
            "steps": [
                {"action_type": "mouse_click", "x": 100, "y": 200}
            ]
        }
        response = self.client.post("/api/v1/scripts/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("pyautogui.click", response.json()["script_code"])

if __name__ == "__main__":
    unittest.main()
