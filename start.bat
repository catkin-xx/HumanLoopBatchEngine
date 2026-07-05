@echo off
cd /d "%~dp0"

echo ========================================
echo windows Launcher
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install from python.org
    pause
    exit /b
)

if not exist "venv" (
    echo [*] Setting up environment...
    python -m venv venv
)
call venv\Scripts\activate

python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing dependencies...
    pip install -r requirements.txt
)

echo [*] Launching PromptMill...
start "" http://localhost:8501
python -m streamlit run app.py
pause