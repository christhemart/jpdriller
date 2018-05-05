@echo off
start cmd /C python manage.py runserver
timeout 2
start http://127.0.0.1:8000/jpdriller/
