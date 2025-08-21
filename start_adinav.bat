@echo off
echo ========================================
echo    AdinavAI Family System Startup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if Ollama is available
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not installed or not in PATH
    echo Please install Ollama from https://ollama.ai
    pause
    exit /b 1
)

echo Starting AdinavAI Family System...
echo.

REM Start the Python startup script
python start_adinav.py

echo.
echo AdinavAI has stopped.
pause
