"""
AutoMacro Desktop Mouse Position Assistant (Tkinter GUI Overlay)
Run this script locally on Windows/Mac/Linux to see live mouse coordinates anywhere outside the browser!
"""
import time
import sys
import threading

try:
    import pyautogui
except ImportError:
    print("Installing pyautogui...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

try:
    import tkinter as tk
except ImportError:
    tk = None

def run_gui_overlay():
    if not tk:
        run_cli_tracker()
        return

    root = tk.Tk()
    root.title("AutoMacro - OS Mouse Tracker")
    root.geometry("320x90+50+50")
    root.attributes("-topmost", True)  # Always on top
    root.configure(bg="#0b0e14")
    root.resizable(False, False)

    label_title = tk.Label(root, text="📍 Real OS Desktop Mouse Position", font=("Inter", 9, "bold"), fg="#58a6ff", bg="#0b0e14")
    label_title.pack(pady=(8, 2))

    label_pos = tk.Label(root, text="X: 0, Y: 0", font=("Fira Code", 16, "bold"), fg="#3fb950", bg="#0b0e14")
    label_pos.pack()

    running = True

    def update_coords():
        while running:
            try:
                x, y = pyautogui.position()
                label_pos.config(text=f"X: {x}, Y: {y}")
            except Exception:
                pass
            time.sleep(0.05)

    t = threading.Thread(target=update_coords, daemon=True)
    t.start()

    def on_closing():
        nonlocal running
        running = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def run_cli_tracker():
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
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n\nTracking stopped.")

if __name__ == "__main__":
    run_gui_overlay()
