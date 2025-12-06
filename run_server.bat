@echo off
cd /d "%~dp0"
echo Starting Django Emergency Ambulance System...
echo.
echo Server will be available at: http://127.0.0.1:8000
echo.
timeout /t 2 /nobreak
start http://127.0.0.1:8000
python manage.py runserver 127.0.0.1:8000
pause
