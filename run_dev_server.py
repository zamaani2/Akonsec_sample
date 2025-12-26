#!/usr/bin/env python
"""
Simple development server runner script.
"""

import os
import sys
import subprocess

# Set DEBUG to True for development
os.environ["DEBUG"] = "True"

# Get the Django manage.py command
manage_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manage.py")

# Default port
port = 8000
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port: {sys.argv[1]}, using default port 8000")

# Run the development server
print(f"Starting development server on port {port}")
print(f"Access your site at: http://127.0.0.1:{port}")

# Command to run
cmd = [sys.executable, manage_py, "runserver", f"0.0.0.0:{port}"]

try:
    # Run the server
    subprocess.run(cmd)
except KeyboardInterrupt:
    print("\nDevelopment server stopped")
