@echo off
echo Starting PromptCAD MVP services...

REM Load environment from .env file
if exist .env (
    for /f "delims=" %%x in (.env) do (set "%%x")
) else (
    echo Warning: .env file not found. Please copy .env.example to .env
    echo and add your OPENAI_API_KEY
    pause
    exit /b 1
)

REM Check for OPENAI_API_KEY
if "%OPENAI_API_KEY%"=="" (
    echo ERROR: OPENAI_API_KEY not set in .env file
    pause
    exit /b 1
)

echo Starting services in new windows...

REM Start LLM Orchestrator
start "LLM Orchestrator" cmd /k "cd services\llm-orchestrator && go run cmd\server\main.go"
timeout /t 2 /nobreak >nul

REM Start Geometry Executor
start "Geometry Executor" cmd /k "cd services\geometry-exec && go run cmd\server\main.go"
timeout /t 2 /nobreak >nul

REM Start API Gateway
start "API Gateway" cmd /k "cd apps\api-gateway && go run cmd\server\main.go"
timeout /t 2 /nobreak >nul

REM Start Viewer Web
start "Viewer Web" cmd /k "cd apps\viewer-web && npm run dev"

echo.
echo ================================================
echo PromptCAD MVP is running!
echo ================================================
echo Viewer Web:         http://localhost:5173
echo API Gateway:        http://localhost:8000
echo LLM Orchestrator:   http://localhost:8001
echo Geometry Executor:  http://localhost:8002
echo ================================================
echo.
echo Close the individual service windows to stop them.
pause
