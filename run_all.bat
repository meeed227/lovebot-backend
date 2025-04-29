@echo off
cd /d %~dp0
echo 🚀 Starting FastAPI server...
start cmd /k uvicorn app:app --reload

timeout /t 2 >nul

echo 🤖 Starting Discord bot...
start cmd /k py -3.10 bot.py
