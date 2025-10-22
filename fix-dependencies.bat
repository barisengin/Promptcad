@echo off
echo ================================================
echo Fixing PromptCAD Dependencies
echo ================================================
echo.

echo [1/3] Fixing LLM Orchestrator...
cd services\llm-orchestrator
go mod tidy
if %errorlevel% neq 0 (
    echo ERROR: Failed to fix llm-orchestrator
    pause
    exit /b 1
)
cd ..\..
echo Done: llm-orchestrator fixed
echo.

echo [2/3] Fixing Geometry Executor...
cd services\geometry-exec
go mod tidy
if %errorlevel% neq 0 (
    echo ERROR: Failed to fix geometry-exec
    pause
    exit /b 1
)
cd ..\..
echo Done: geometry-exec fixed
echo.

echo [3/3] Fixing API Gateway...
cd apps\api-gateway
go mod tidy
if %errorlevel% neq 0 (
    echo ERROR: Failed to fix api-gateway
    pause
    exit /b 1
)
cd ..\..
echo Done: api-gateway fixed
echo.

echo ================================================
echo All Dependencies Fixed!
echo ================================================
echo.
echo Now run: scripts\start-dev.bat
echo.
pause
