@echo off
REM LinkedIn Post Automation Tool - Dynamic Deployment Script (Windows)
REM This script sets up the complete Python + Selenium environment

echo.
echo 🚀 LinkedIn Post Automation Tool - Dynamic Deployment
echo ======================================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% found

REM Check if pip is installed
echo [INFO] Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip not found. Please install pip
    pause
    exit /b 1
)
echo [SUCCESS] pip found

REM Create virtual environment
echo [INFO] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo [SUCCESS] Virtual environment activated

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo [INFO] Installing Python requirements...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo [SUCCESS] Requirements installed successfully
) else (
    echo [ERROR] requirements.txt not found
    pause
    exit /b 1
)

REM Check Chrome installation
echo [INFO] Checking Google Chrome installation...
where chrome >nul 2>&1
if %errorlevel% neq 0 (
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        echo [SUCCESS] Chrome found at C:\Program Files\Google\Chrome\Application\chrome.exe
    ) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        echo [SUCCESS] Chrome found at C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
    ) else (
        echo [WARNING] Chrome not found. Please install from https://www.google.com/chrome/
        echo [WARNING] The scraper will use mock data without Chrome
    )
) else (
    echo [SUCCESS] Chrome found in PATH
)

REM Run setup script
echo [INFO] Running setup script...
if exist "setup.py" (
    python setup.py
    echo [SUCCESS] Setup completed
) else (
    echo [ERROR] setup.py not found
    pause
    exit /b 1
)

REM Test installation
echo [INFO] Testing installation...
if exist "test_setup.py" (
    python test_setup.py
    if %errorlevel% equ 0 (
        echo [SUCCESS] Installation test passed
    ) else (
        echo [WARNING] Installation test failed, but continuing...
    )
) else (
    echo [WARNING] test_setup.py not found, skipping test
)

REM Display completion message
echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Application Details:
echo    • Tool: LinkedIn Post Automation with Python + Selenium
echo    • UI: Streamlit Web Interface  
echo    • Features: Dynamic web scraping, real-time data extraction
echo    • URL: http://localhost:8501
echo.
echo 🚀 Starting the application...
echo    Press Ctrl+C to stop the server
echo.

REM Start Streamlit app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

echo.
echo [SUCCESS] Deployment completed successfully!
pause