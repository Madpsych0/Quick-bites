#!/usr/bin/env python
"""
Convenience script to run the scanner app on port 8001
Usage: python run_scanner.py
"""
import os
import sys
import subprocess

def main():
    """Run the scanner Django app on port 8001"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scanner_project.settings')
    
    try:
        # Run the scanner app on port 8001
        subprocess.run([
            sys.executable, 'scanner_manage.py', 'runserver', '0.0.0.0:8001'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running scanner app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nScanner app stopped.")
        sys.exit(0)

if __name__ == '__main__':
    main()
