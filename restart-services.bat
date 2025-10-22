@echo off
echo ================================================
echo Restarting PromptCAD Services
echo ================================================
echo.
echo Please close all existing service windows first!
echo.
pause
echo.
echo Starting services...
call scripts\start-dev.bat
