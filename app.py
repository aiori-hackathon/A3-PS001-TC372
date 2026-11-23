"""
Top-level entry point redirecting to Dashboard/app.py.
Allows running: streamlit run app.py
"""

import os
import sys

# Ensure Dashboard directory is in path and execute app.py
dashboard_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dashboard")
sys.path.insert(0, dashboard_dir)

# Execute Dashboard/app.py
app_path = os.path.join(dashboard_dir, "app.py")
with open(app_path) as f:
    code = compile(f.read(), app_path, 'exec')
    exec(code)
