@echo off
setlocal
set "VENV_DIR=venv"
set "ROOT_DIR=.."
set "SETUP_DIR=%~dp0"
set "PROJECT_ROOT="
set "CURRENT_DIR="

REM --- Check Execution Location ---

REM Get the absolute path of the Project Root
pushd .
cd /d "%SETUP_DIR%"
cd /d "%ROOT_DIR%"
set "PROJECT_ROOT=%CD%"
popd

set "CURRENT_DIR=%CD%"

IF NOT "%CURRENT_DIR%"=="%PROJECT_ROOT%" (
    ECHO [FATAL ERROR] ----------------------------------------
    ECHO This setup file must be executed from the Project Root Directory.
    ECHO Current Location: "%CURRENT_DIR%"
    ECHO Correct Execution Path: "%PROJECT_ROOT%"
    ECHO Example Command: setup\setup.bat
    ECHO ----------------------------------------
    EXIT /B 1
)

REM --- Move to setup directory for requirements.txt ---
pushd .
cd /d "%SETUP_DIR%" 

ECHO ----------------------------------------
ECHO 1. Starting setup for Windows...
ECHO ----------------------------------------

REM Create venv in the root directory
python -m venv "%ROOT_DIR%\%VENV_DIR%"
if errorlevel 1 goto :error_python

ECHO ----------------------------------------
ECHO 2. Activating venv and installing packages...
ECHO ----------------------------------------

call "%ROOT_DIR%\%VENV_DIR%\Scripts\activate"
if errorlevel 1 goto :error_venv_activate

REM Install packages from requirements.txt (in the current dir: setup/)
pip install -r "requirements.txt"
if errorlevel 1 goto :error_pip_install

ECHO ----------------------------------------
ECHO Setup successful. Creating run.bat in the root directory.
ECHO ----------------------------------------

REM Create run.bat in the root directory
(
ECHO @echo off
ECHO call "%VENV_DIR%\Scripts\activate"
ECHO python src\main.py %%*
ECHO call deactivate
) > "%ROOT_DIR%\run.bat"

deactivate
popd
goto :eof

:error_python
ECHO [ERROR] Python not found or failed to create venv.
popd
endlocal
goto :eof
:error_venv_activate
ECHO [ERROR] Failed to activate venv.
popd
endlocal
goto :eof
:error_pip_install
ECHO [ERROR] Failed to install packages. Check requirements.txt.
popd
endlocal
goto :eof