@echo off
REM Change to the script directory
cd %~dp0

REM Django setup
cd backend\aiLingo
IF NOT EXIST .venv (
    python -m venv .venv
)
.venv\Scripts\activate
pip install -r requirements.txt
echo Starting Django server...
start /b python manage.py runserver

REM Next.js setup
cd ..\..\frontend\aiLingo
echo Starting Next.js server...
npm install
start npm run dev

REM Keep the script window open
pause
