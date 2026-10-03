@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "GAME_FILE=%~dp0game.py"

where py >nul 2>nul
if errorlevel 1 (
    echo Python 3.12 is required for this game, but the Windows launcher is not available.
    echo Please install Python 3.12.x from: https://www.python.org/downloads/windows/
    echo Make sure the Python launcher is installed.
    pause
    exit /b 1
)

py -3.12 -c "import sys; print(sys.version)" >nul 2>nul
if errorlevel 1 (
    echo Python 3.12 is required for this game.
    echo It was not found on this computer.
    echo Please install Python 3.12.x from: https://www.python.org/downloads/windows/
    echo Then run this launcher again.
    pause
    exit /b 1
)

echo Using Python 3.12...
py -3.12 -m pip install --upgrade pip setuptools wheel
py -3.12 -m pip install pygame
py -3.12 "%GAME_FILE%"
exit /b %ERRORLEVEL%