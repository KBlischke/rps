@echo off
set "PROJECT_PATH=%~dp0"
cd /d %PROJECT_PATH%
set FLASK_APP=app.py
set FLASK_ENV=production
start /B http://127.0.0.1:5000/
flask run
