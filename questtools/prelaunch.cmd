@echo off
rem Prism pre-launch hook. Runs the pack checker (validate.py) only when Python 3.11+ is installed;
rem on PCs without Python the check is skipped and the game starts normally.
where py >nul 2>nul
if errorlevel 1 goto nopython
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>nul
if errorlevel 1 goto nopython
py -3 "%~dp0validate.py"
exit /b %errorlevel%
:nopython
echo [Elysius] Python 3.11+ not found - skipping the pack check (only needed for pack development).
exit /b 0
