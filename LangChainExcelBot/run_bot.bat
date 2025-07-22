@echo off
start cmd /k "ollama run mistral"
timeout /t 5
start cmd /k "cd /d C:\Users\theab\OneDrive\Desktop\Semester Project\LangChainExcelBot && python app.py"