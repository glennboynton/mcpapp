@echo off
REM windows_run_all_dev.bat - Root of project (.\windows_run_all_dev.bat)
REM Start Flask dev server AND Docusaurus dev server on Windows using venv .\mcpapp.

REM =============================================================================
REM Requirements:
REM   - Python + virtualenv in .\mcpapp (created with: python -m venv mcpapp)
REM   - All Python deps installed into that venv:
REM       mcpapp\Scripts\activate
REM       pip install -r requirements.txt
REM   - Node.js + npm (only if you still use live Docusaurus dev)
REM =============================================================================

setlocal ENABLEDELAYEDEXECUTION

REM ---- Check venv exists ------------------------------------------------------
if not exist "Scripts\activate.bat" (
    echo [windows_run_all_dev] ERROR: .\mcpapp virtual environment not found.
    echo   Create it with:
    echo     python -m venv mcpapp
    echo     mcpapp\Scripts\activate
    echo     pip install -r requirements.txt
    goto :end
)

REM ---- Start Flask in a new window (with venv activated) ----------------------
echo [windows_run_all_dev] Starting Flask dev server on http://localhost:5000 ...
set FLASK_ENV=development
set FLASK_APP=app.py
start "Flask Dev Server" cmd /k "call Scripts\activate.bat && python app.py"

REM ---- Start Docusaurus in a new window (optional; requires npm) -------------
if not exist "docs" (
    echo [windows_run_all_dev] WARNING: .\docs directory not found.
    echo   Skipping Docusaurus dev server.
    goto :show_urls
)

echo [windows_run_all_dev] Starting Docusaurus dev server on http://localhost:3000 ...
pushd docs
start "Docusaurus Dev Server" cmd /k "npm start"
popd

:show_urls
echo.
echo [windows_run_all_dev] Dev servers started (where available).
echo   Flask:      http://localhost:5000
echo   Docusaurus: http://localhost:3000  (if docs/ exists and npm is installed)
echo.
echo Close the opened Command Prompt windows to stop each server.

:end
endlocal
