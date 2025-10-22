@echo off
set TENANT=%1
if "%TENANT%"=="" set TENANT=cliente_a
set ENV_FILE=tenants\%TENANT%.env
for /f "tokens=1,* delims==" %%a in ('findstr /b "PROMPTS_FILE=" %ENV_FILE%') do set PROMPTS_FILE=%%b
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000