@echo off
REM Smart Gold Trading Dashboard - Windows Startup Script

echo 🏆 Starting Smart Gold Trading Dashboard...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo 📥 Installing/updating dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Launching dashboard...
echo.
echo 📌 Login credentials:
echo    Username: demo
echo    Password: demo123
echo.

REM Run Streamlit
streamlit run main.py

