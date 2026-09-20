@echo off
title CivicAlert AI - Push to GitHub
echo ========================================================
echo Pushing CivicAlert AI to GitHub
echo Repository: https://github.com/zahidjan01a/AI-Powered-Public-Infrastructure-Issue-Detection-and-Reporting-System
echo ========================================================
echo.

set PATH=%LOCALAPPDATA%\Programs\MinGit\cmd;%PATH%

echo 1. Verifying Git...
git --version
if %errorlevel% neq 0 (
    echo Error: Git not found.
    pause
    exit /b %errorlevel%
)

echo.
echo 2. Pushing main branch to GitHub...
git push -u origin main --force

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo SUCCESS! All files pushed to your GitHub repository!
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo Push encountered an authentication or repository error.
    echo Note: Ensure the repository exists at:
    echo https://github.com/zahidjan01a/AI-Powered-Public-Infrastructure-Issue-Detection-and-Reporting-System
    echo ========================================================
)

echo.
pause
