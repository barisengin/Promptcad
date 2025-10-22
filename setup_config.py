import os

files = {
    ".env.example": '''# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Service Ports
API_GATEWAY_PORT=8000
LLM_ORCHESTRATOR_PORT=8001
GEOMETRY_EXEC_PORT=8002
VIEWER_WEB_PORT=5173

# Service URLs (for development)
LLM_ORCHESTRATOR_URL=http://localhost:8001
GEOMETRY_EXEC_URL=http://localhost:8002
''',

    "Makefile": '''# PromptCAD MVP Makefile

.PHONY: help install dev clean

help:
	@echo "PromptCAD MVP Commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make dev         - Start all services for development"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make test        - Run tests (future)"

install:
	@echo "Installing dependencies..."
	cd apps/viewer-web && npm install
	cd packages/dsl-schema && npm install
	cd services/llm-orchestrator && go mod download
	cd services/geometry-exec && go mod download
	cd apps/api-gateway && go mod download
	@echo "Installation complete!"

dev:
	@echo "Starting PromptCAD MVP..."
	@echo "Make sure you have set OPENAI_API_KEY in .env file"
	@bash scripts/start-dev.sh

clean:
	@echo "Cleaning build artifacts..."
	rm -rf apps/viewer-web/dist
	rm -rf apps/viewer-web/node_modules
	rm -rf packages/dsl-schema/node_modules
	@echo "Clean complete!"

test:
	@echo "Running tests..."
	@echo "Tests not yet implemented"
''',

    "scripts/start-dev.sh": '''#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Warning: .env file not found. Using defaults."
    echo "Please copy .env.example to .env and add your OPENAI_API_KEY"
fi

# Check for required environment variables
if [ -z "$OPENAI_API_KEY" ]; then
    echo "ERROR: OPENAI_API_KEY not set in .env file"
    exit 1
fi

echo "Starting PromptCAD MVP services..."

# Start LLM Orchestrator
cd services/llm-orchestrator
echo "Starting LLM Orchestrator on port 8001..."
go run cmd/server/main.go &
LLM_PID=$!
cd ../..

# Wait a bit for service to start
sleep 2

# Start Geometry Executor
cd services/geometry-exec
echo "Starting Geometry Executor on port 8002..."
go run cmd/server/main.go &
GEOM_PID=$!
cd ../..

# Wait a bit for service to start
sleep 2

# Start API Gateway
cd apps/api-gateway
echo "Starting API Gateway on port 8000..."
go run cmd/server/main.go &
API_PID=$!
cd ../..

# Wait a bit for service to start
sleep 2

# Start Viewer Web
cd apps/viewer-web
echo "Starting Viewer Web on port 5173..."
npm run dev &
WEB_PID=$!
cd ../..

echo ""
echo "================================================"
echo "PromptCAD MVP is running!"
echo "================================================"
echo "Viewer Web:         http://localhost:5173"
echo "API Gateway:        http://localhost:8000"
echo "LLM Orchestrator:   http://localhost:8001"
echo "Geometry Executor:  http://localhost:8002"
echo "================================================"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C and kill all processes
trap "echo 'Stopping services...'; kill $LLM_PID $GEOM_PID $API_PID $WEB_PID 2>/dev/null; exit" INT

# Wait for all processes
wait
''',

    "scripts/start-dev.bat": '''@echo off
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
''',

    ".gitignore": '''# Dependencies
node_modules/
vendor/

# Build outputs
dist/
build/
*.exe
*.dll
*.so
*.dylib

# Go
*.test
*.out
go.work

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
''',
}

base_path = r"C:\Users\baris\Downloads\promptcad"
for file_path, content in files.items():
    full_path = os.path.join(base_path, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {file_path}")

print("\nConfiguration files created successfully!")
