import subprocess
import time
import os
import sys

# --- Configuration ---
QUICKBITES_PORT = 8000
SCANNER_PORT = 8001
HOST_IP = "0.0.0.0" # Use 0.0.0.0 to allow network access

# --- Paths ---
# Assumes the script is in the root directory alongside manage.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUICKBITES_MANAGE_PY = os.path.join(BASE_DIR, "manage.py")
SCANNER_MANAGE_PY = os.path.join(BASE_DIR, "manage.py") # Adjust if they are in different locations

def print_header():
    print("--- Starting Canteen Digitalization Project ---")

def print_footer(processes):
    print(f"✅ Starting QuickBites server on http://127.0.0.1:{QUICKBITES_PORT}")
    print(f"✅ Starting Scanner server on http://127.0.0.1:{SCANNER_PORT}")
    print("-" * 48)
    print("🛑 Ctrl+C to stop both servers.")
    print("-" * 48)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping both servers...")
        for p in processes:
            p.terminate()
        print("🛑 Servers stopped")

def start_servers():
    print_header()

    # Command for QuickBites Server
    quickbites_command = [
        sys.executable,
        QUICKBITES_MANAGE_PY,
        "runserver",
        f"{HOST_IP}:{QUICKBITES_PORT}",
        "--settings=quickbites.settings" # Specify settings file
    ]

    # Command for Scanner Server
    scanner_command = [
        sys.executable,
        SCANNER_MANAGE_PY,
        "runserver",
        f"{HOST_IP}:{SCANNER_PORT}",
        "--settings=scanner_project.settings" # Specify settings file
    ]

    # Start both processes
    processes = [
        subprocess.Popen(quickbites_command),
        subprocess.Popen(scanner_command)
    ]

    print_footer(processes)

if __name__ == "__main__":
    start_servers()