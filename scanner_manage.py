#!/usr/bin/env python
"""Django's command-line utility for scanner app on port 8001."""
import os
import sys

def main():
    """Run scanner app on port 8001."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scanner_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Override sys.argv to run on port 8001
    if len(sys.argv) == 2 and sys.argv[1] == 'runserver':
        sys.argv = ['scanner_manage.py', 'runserver', '0.0.0.0:8001']
    elif len(sys.argv) == 1:
        sys.argv = ['scanner_manage.py', 'runserver', '0.0.0.0:8001']
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
