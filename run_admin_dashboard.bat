@echo off
title CivicAlert AI - Municipal Admin Operations Console
echo ========================================================
echo Launching CivicAlert AI - Municipal Operations Console (Port 8502)
echo ========================================================
python -m streamlit run app/admin_dashboard.py --server.port 8502
pause
