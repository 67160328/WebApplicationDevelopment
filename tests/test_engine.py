import unittest
from app.engine.script_engine import ScriptEngine
from app.schemas.action_schema import AutomationStep, ActionType
from app.core.exceptions import UnsupportedLanguageException

class TestScriptEngine(unittest.TestCase):

    def test_python_generation(self):
        engine = ScriptEngine()
        steps = [
            AutomationStep(action_type=ActionType.MOUSE_CLICK, x=100, y=200),
            AutomationStep(action_type=ActionType.DELAY, duration_ms=1000),
            AutomationStep(action_type=ActionType.KEY_BINDING, key="enter")
        ]
        code, ext = engine.generate_script("python", steps)
        self.assertEqual(ext, ".py")
        self.assertIn("pyautogui.click(x=100, y=200)", code)
        self.assertIn("time.sleep(1.0)", code)
        self.assertIn("pyautogui.press('enter')", code)

    def test_ahk_generation(self):
        engine = ScriptEngine()
        steps = [
            AutomationStep(action_type=ActionType.MOUSE_CLICK, x=50, y=75),
            AutomationStep(action_type=ActionType.DELAY, duration_ms=500),
            AutomationStep(action_type=ActionType.KEY_BINDING, key="a")
        ]
        code, ext = engine.generate_script("ahk", steps)
        self.assertEqual(ext, ".ahk")
        self.assertIn("Click, 50, 75", code)
        self.assertIn("Sleep, 500", code)
        self.assertIn("Send, {a}", code)

    def test_bash_generation(self):
        engine = ScriptEngine()
        steps = [
            AutomationStep(action_type=ActionType.MOUSE_CLICK, x=10, y=20),
            AutomationStep(action_type=ActionType.DELAY, duration_ms=2000),
            AutomationStep(action_type=ActionType.KEY_BINDING, key="ctrl+c")
        ]
        code, ext = engine.generate_script("bash", steps)
        self.assertEqual(ext, ".sh")
        self.assertIn("xdotool mousemove 10 20 click 1", code)
        self.assertIn("sleep 2.0", code)
        self.assertIn("xdotool key ctrl+c", code)

    def test_unsupported_language(self):
        engine = ScriptEngine()
        with self.assertRaises(UnsupportedLanguageException):
            engine.generate_script("unsupported_lang", [])

if __name__ == "__main__":
    unittest.main()
