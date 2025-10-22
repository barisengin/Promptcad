# PromptCAD MVP - Execution Checklist

## Before You Start

### 1. Install Prerequisites

- [ ] **Go 1.21+** installed
  ```bash
  go version  # Should show 1.21 or higher
  ```

- [ ] **Node.js 18+** installed
  ```bash
  node --version  # Should show v18.x.x or higher
  npm --version   # Should show 9.x.x or higher
  ```

- [ ] **OpenAI API Key** obtained
  - Visit: https://platform.openai.com/api-keys
  - Create new API key
  - Copy key (starts with `sk-`)

### 2. Configure Environment

- [ ] Copy environment template
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` file and add your API key
  ```
  OPENAI_API_KEY=sk-your-actual-key-here
  ```

### 3. Install Dependencies

- [ ] Run installation command
  ```bash
  make install
  ```
  
  **OR** if `make` not available, run manually:
  ```bash
  cd apps/viewer-web && npm install && cd ../..
  cd packages/dsl-schema && npm install && cd ../..
  cd services/llm-orchestrator && go mod download && cd ../..
  cd services/geometry-exec && go mod download && cd ../..
  cd apps/api-gateway && go mod download && cd ../..
  ```

## Starting the MVP

### Option 1: Automated Start (Recommended)

**Windows:**
- [ ] Run startup script
  ```bash
  scripts\start-dev.bat
  ```
- [ ] Wait for 4 terminal windows to open
- [ ] Check each window for startup messages

**Linux/Mac:**
- [ ] Make script executable
  ```bash
  chmod +x scripts/start-dev.sh
  ```
- [ ] Run startup script
  ```bash
  ./scripts/start-dev.sh
  ```

### Option 2: Manual Start

Open **4 separate terminals** and run these commands:

**Terminal 1: LLM Orchestrator**
- [ ] Start service
  ```bash
  cd services/llm-orchestrator
  go run cmd/server/main.go
  ```
- [ ] Wait for: "LLM Orchestrator running on :8001"

**Terminal 2: Geometry Executor**
- [ ] Start service
  ```bash
  cd services/geometry-exec
  go run cmd/server/main.go
  ```
- [ ] Wait for: "Geometry Executor running on :8002"

**Terminal 3: API Gateway**
- [ ] Start service
  ```bash
  cd apps/api-gateway
  go run cmd/server/main.go
  ```
- [ ] Wait for: "API Gateway running on :8000"

**Terminal 4: Viewer Web**
- [ ] Start service
  ```bash
  cd apps/viewer-web
  npm run dev
  ```
- [ ] Wait for: "Local: http://localhost:5173/"

## Verification Steps

### 1. Check Service Health

- [ ] **LLM Orchestrator health check**
  ```bash
  curl http://localhost:8001/health
  ```
  Expected: `{"status":"healthy"}`

- [ ] **Geometry Executor health check**
  ```bash
  curl http://localhost:8002/health
  ```
  Expected: `{"status":"healthy"}`

- [ ] **API Gateway health check**
  ```bash
  curl http://localhost:8000/api/health
  ```
  Expected: `{"status":"healthy"}`

### 2. Test LLM Service

- [ ] Test prompt parsing
  ```bash
  curl -X POST http://localhost:8001/parse \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Create a box 10mm wide, 20mm tall, 5mm deep"}'
  ```
  Expected: JSON with "version" and "operations" fields

### 3. Test Geometry Service

- [ ] Test DSL execution
  ```bash
  curl -X POST http://localhost:8002/execute \
    -H "Content-Type: application/json" \
    -d '{"version":"1.0","operations":[{"id":"op1","type":"box","params":{"width":10,"height":20,"depth":5}}]}'
  ```
  Expected: JSON with "geometry" field

### 4. Test Full Pipeline

- [ ] Test end-to-end flow
  ```bash
  curl -X POST http://localhost:8000/api/prompt \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Create a box 100mm wide, 50mm tall, 30mm deep"}'
  ```
  Expected: JSON with "dsl" and "geometry" fields

### 5. Access Web Interface

- [ ] Open browser to: http://localhost:5173
- [ ] Verify you see:
  - Left panel with "PromptCAD" title
  - Text area for prompt input
  - "Generate Model" button
  - Right panel with 3D grid view

### 6. Test Web UI Functionality

- [ ] Enter prompt: "Create a box 100mm wide, 50mm tall, 30mm deep"
- [ ] Click "Generate Model" button
- [ ] Wait for response (5-10 seconds)
- [ ] Check for geometry JSON in left panel
- [ ] Open browser console (F12)
- [ ] Verify no error messages

## Troubleshooting Checklist

If something doesn't work, check these:

- [ ] All 4 services are running (check terminals)
- [ ] No "port already in use" errors
- [ ] OPENAI_API_KEY is set correctly in .env
- [ ] No firewall blocking localhost ports
- [ ] Node.js and Go versions meet requirements
- [ ] Dependencies installed without errors

## Common Issues

### Issue: "OPENAI_API_KEY not set"
- [ ] Check .env file exists (not .env.example)
- [ ] Verify API key starts with "sk-"
- [ ] Restart services after editing .env

### Issue: Port already in use
- [ ] Kill existing processes on ports 8000, 8001, 8002, 5173
  ```bash
  # Windows: netstat -ano | findstr :8000
  # Linux/Mac: lsof -ti:8000 | xargs kill -9
  ```

### Issue: Go module errors
- [ ] Run `go mod tidy` in each service directory
- [ ] Check internet connection for downloads

### Issue: npm install fails
- [ ] Delete node_modules and package-lock.json
- [ ] Run `npm cache clean --force`
- [ ] Run `npm install` again

## Success Indicators

You've successfully set up the MVP when:

- ✅ All 4 services running without errors
- ✅ All health checks return `{"status":"healthy"}`
- ✅ Full pipeline test returns DSL + geometry JSON
- ✅ Web interface loads at localhost:5173
- ✅ Can enter prompt and get response
- ✅ Browser console shows no errors

## What to Do Next

Once everything is working:

1. **Experiment with prompts** - Try different box dimensions
2. **Review the code** - Understand the architecture
3. **Check logs** - See how services communicate
4. **Read documentation** - README.md and SETUP.md
5. **Plan enhancements** - See roadmap in README.md

## Getting Help

If you're stuck:

1. Check SETUP.md for detailed troubleshooting
2. Review service logs for error messages
3. Verify all prerequisites are installed
4. Try manual startup to isolate issues
5. Check GitHub issues or open a new one

---

**Good luck! 🚀**
