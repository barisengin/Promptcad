@echo off
echo ================================================
echo PromptCAD MVP - Installing Dependencies
echo ================================================
echo.

echo [1/5] Installing viewer-web dependencies...
cd apps\viewer-web
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install viewer-web dependencies
    pause
    exit /b 1
)
cd ..\..
echo Done: viewer-web dependencies installed
echo.

echo [2/5] Installing dsl-schema dependencies...
cd packages\dsl-schema
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dsl-schema dependencies
    pause
    exit /b 1
)
cd ..\..
echo Done: dsl-schema dependencies installed
echo.

echo [3/5] Downloading llm-orchestrator Go modules...
cd services\llm-orchestrator
go mod download
if %errorlevel% neq 0 (
    echo ERROR: Failed to download llm-orchestrator modules
    pause
    exit /b 1
)
cd ..\..
echo Done: llm-orchestrator modules downloaded
echo.

echo [4/5] Downloading geometry-exec Go modules...
cd services\geometry-exec
go mod download
if %errorlevel% neq 0 (
    echo ERROR: Failed to download geometry-exec modules
    pause
    exit /b 1
)
cd ..\..
echo Done: geometry-exec modules downloaded
echo.

echo [5/5] Downloading api-gateway Go modules...
cd apps\api-gateway
go mod download
if %errorlevel% neq 0 (
    echo ERROR: Failed to download api-gateway modules
    pause
    exit /b 1
)
cd ..\..
echo Done: api-gateway modules downloaded
echo.

echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Add your OPENAI_API_KEY to .env
echo 3. Run: scripts\start-dev.bat
echo.
pause
