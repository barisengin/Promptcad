#!/bin/bash

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
