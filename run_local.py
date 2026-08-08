"""
Direct Real Windows Mouse Click Runner for AutoMacro
Runs FastAPI directly on your host Windows system so PyAutoGUI can control real mouse pointer clicks!
"""
import os
import sys
import subprocess

def main():
    print("==================================================")
    print(" 🚀 AUTOMACRO - REAL WINDOWS MOUSE CLICK ENGINE")
    print("==================================================")
    
    # 1. Stop Docker container to free up port 8090
    print("\n[1/3] Stopping Docker sandbox container to free port 8090...")
    try:
        subprocess.run(["docker", "compose", "down"], check=False)
    except Exception:
        pass

    # 2. Check/Install PyAutoGUI
    print("\n[2/3] Checking host Python dependencies...")
    try:
        import pyautogui
        import uvicorn
        import fastapi
    except ImportError:
        print("Installing dependencies on Windows Host...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # 3. Launch Uvicorn Server directly on Host Windows
    print("\n[3/3] Starting Local API Server with Real Mouse Control...")
    print("👉 Open your browser at: http://localhost:8090/\n")
    
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)

if __name__ == "__main__":
    main()
