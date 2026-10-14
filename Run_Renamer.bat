@echo off
:: Run the Python script
python "rename srt.py"

:: Check if the Python script threw an error (Exit code not equal to 0)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ----------------------------------------------------
    echo [!] AN ERROR OCCURRED. Please read the message above.
    echo ----------------------------------------------------
    pause
)