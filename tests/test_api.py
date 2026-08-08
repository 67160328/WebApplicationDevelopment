import unittest
from fastapi.testclient import TestClient
from main import app

class TestScriptAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("python", data["supported_languages"])

    def test_generate_script_api(self):
        payload = {
            "target_language": "python",
            "output_name": "test_script",
            "steps": [
                {"action_type": "mouse_click", "x": 100, "y": 150},
                {"action_type": "delay", "duration_ms": 1000}
            ]
        }
        response = self.client.post("/api/v1/scripts/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["target_language"], "python")
        self.assertEqual(data["file_extension"], ".py")
        self.assertIn("pyautogui.click(x=100, y=150)", data["script_code"])

    def test_export_script_api(self):
        payload = {
            "target_language": "ahk",
            "output_name": "my_ahk_macro",
            "steps": [
                {"action_type": "mouse_click", "x": 50, "y": 60}
            ]
        }
        response = self.client.post("/api/v1/scripts/export", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-disposition"], 'attachment; filename="my_ahk_macro.ahk"')
        self.assertIn("Click, 50, 60", response.text)

if __name__ == "__main__":
    unittest.main()
