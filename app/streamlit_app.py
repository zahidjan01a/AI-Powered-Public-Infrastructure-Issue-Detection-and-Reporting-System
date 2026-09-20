"""
Streamlit Application Entrypoint
AI-Powered Public Infrastructure Issue Detection and Reporting System

This file serves as an entrypoint alias for `app/app.py` to support standard
deployment conventions (e.g. `streamlit run app/streamlit_app.py` or `streamlit run app/app.py`).
"""

import runpy
from pathlib import Path

APP_FILE = Path(__file__).resolve().parent / "app.py"

if __name__ == "__main__":
    runpy.run_path(str(APP_FILE), run_name="__main__")
