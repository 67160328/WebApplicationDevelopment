"""
Standalone Native Desktop Mouse Tracker Utility
Run this script locally on your OS desktop to inspect real mouse coordinates anywhere!
"""
import time
import sys

try:
    import pyautogui
except ImportError:
    print("Installing pyautogui...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

def start_desktop_tracking():
    print("==================================================")
    print(" 📍 LIVE OS DESKTOP MOUSE POSITION TRACKER")
    print(" Move your mouse anywhere on your Desktop screen!")
    print(" Press Ctrl+C to stop tracking.")
    print("==================================================\n")
    try:
        while True:
            x, y = pyautogui.position()
            position_str = f"X: {str(x).rjust(4)} | Y: {str(y).rjust(4)}"
            print(f"\r📍 Current Desktop Mouse Position: {position_str}", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nTracking stopped.")

if __name__ == "__main__":
    start_desktop_tracking()
