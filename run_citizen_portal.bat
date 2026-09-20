@echo off
title CivicAlert AI - Public Citizen Portal
echo ========================================================
echo Launching CivicAlert AI - Public Citizen Portal (Port 8501)
echo ========================================================
python -m streamlit run app/app.py --server.port 8501
pause
