@echo off
echo ========================================================
echo Starting JanRakshak AI (CivicShield) - PromptWars Edition
echo ========================================================
echo Opening at http://127.0.0.1:8000
echo.
.venv\Scripts\python.exe -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
pause
