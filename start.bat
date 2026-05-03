@echo off
title OneDisc Bot
echo ==========================================
echo           OneDisc Bot Starter
echo ==========================================
echo.
echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

echo Starting OneDisc...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application crashed.
    pause
)
pause
