# PromptCAD MVP - Setup & Execution Guide

## Step-by-Step Setup Instructions

### Prerequisites Check

Before starting, ensure you have:

1. **Go 1.21+**
   ```bash
   go version
   # Should show: go version go1.21.x or higher
   ```

2. **Node.js 18+**
   ```bash
   node --version
   # Should show: v18.x.x or higher
   ```

3. **npm**
   ```bash
   npm --version
   # Should show: 9.x.x or higher
   ```

4. **OpenAI API Key**
   - Sign up at https://platform.openai.com/
   - Create an API key at https://platform.openai.com/api-keys

---

## Installation Steps

### Step 1: Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# Replace "your-openai-api-key-here" with your actual key
```

On Windows, you can use:
```bash
notepad .env
```

On Linux/Mac:
```bash
nano .env
# or
vim .env
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx...
```

### Step 2: Install Dependencies

Run the following command in the project root:

```bash
make install
```

This will:
1. Install npm packages for the web viewer (React + Three.js)
2. Install npm packages for the DSL schema package
3. Download Go module dependencies for all 3 backend services

**Expected output:**
```
Installing dependencies...
cd apps/viewer-web && npm install
...
cd packages/dsl-schema && npm install
...
cd services/llm-orchestrator && go mod download
...
cd services/geometry-exec && go mod download
...
cd apps/api-gateway && go mod download
Installation complete!
```

**If you don't have `make` installed:**

Run these commands manually:

```bash
# Install frontend dependencies
cd apps/viewer-web && npm install && cd ../..
cd packages/dsl-schema && npm install && cd ../..

# Install Go dependencies
cd services/llm-orchestrator && go mod download && cd ../..
cd services/geometry-exec && go mod download && cd ../..
cd apps/api-gateway && go mod download && cd ../..
```

---

## Running the MVP

### Option 1: Start All Services (Recommended)

**On Windows:**
```bash
scripts\start-dev.bat
```

This will open 4 terminal windows, one for each service.

**On Linux/Mac:**
```bash
chmod +x scripts/start-dev.sh
./scripts/start-dev.sh
```

This will start all services in the background.

### Option 2: Start Services Manually

If the automated script doesn't work, start each service in a separate terminal:

**Terminal 1 - LLM Orchestrator:**
```bash
cd services/llm-orchestrator
set OPENAI_API_KEY=sk-your-key-here  # Windows
# export OPENAI_API_KEY=sk-your-key-here  # Linux/Mac
go run cmd/server/main.go
```

**Terminal 2 - Geometry Executor:**
```bash
cd services/geometry-exec
go run cmd/server/main.go
```

**Terminal 3 - API Gateway:**
```bash
cd apps/api-gateway
go run cmd/server/main.go
```

**Terminal 4 - Viewer Web:**
```bash
cd apps/viewer-web
npm run dev
```

---

## Verification

### 1. Check Service Health

Open new terminals and run:

```bash
# Test LLM Orchestrator
curl http://localhost:8001/health

# Test Geometry Executor
curl http://localhost:8002/health

# Test API Gateway
curl http://localhost:8000/api/health
```

Each should return: `{"status":"healthy"}`

### 2. Test the Pipeline

```bash
curl -X POST http://localhost:8000/api/prompt \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"Create a box 100mm wide, 50mm tall, 30mm deep\"}"
```

**Expected response:**
```json
{
  "dsl": {
    "version": "1.0",
    "operations": [
      {
        "id": "op1",
        "type": "box",
        "params": {
          "width": 100,
          "height": 50,
          "depth": 30
        }
      }
    ]
  },
  "geometry": "{\"type\":\"box\",\"width\":100.00,\"height\":50.00,\"depth\":30.00}"
}
```

### 3. Access the Web UI

Open your browser to: **http://localhost:5173**

You should see the PromptCAD interface with:
- A text input area on the left
- A 3D viewer with a grid on the right

---

## Usage Examples

Try these prompts in the web interface:

1. **Simple Box:**
   ```
   Create a box 100mm wide, 50mm tall, and 30mm deep
   ```

2. **Different dimensions:**
   ```
   Make a rectangular prism 200mm by 100mm by 75mm
   ```

3. **Cylinder (if LLM generates it):**
   ```
   Create a cylinder with radius 50mm and height 100mm
   ```

---

## Troubleshooting

### Issue: "OPENAI_API_KEY not set"

**Solution:**
1. Check that you created the `.env` file (not `.env.example`)
2. Ensure the key starts with `sk-`
3. No quotes around the key in `.env` file
4. Restart the services after editing `.env`

### Issue: Port Already in Use

**Error message:** `listen tcp :8000: bind: address already in use`

**Solution:**

**Windows:**
```bash
# Find what's using the port
netstat -ano | findstr :8000
# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

### Issue: npm Install Fails

**Solution:**
```bash
cd apps/viewer-web
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Issue: Go Modules Not Found

**Solution:**
```bash
# For each service, run:
cd services/llm-orchestrator
go mod tidy
go mod download

cd ../geometry-exec
go mod tidy
go mod download

cd ../../apps/api-gateway
go mod tidy
go mod download
```

### Issue: CORS Errors in Browser

**Solution:**
- Check that all services are running
- Ensure API Gateway is running on port 8000
- Clear browser cache and reload

### Issue: OpenAI API Rate Limit

**Error:** `Rate limit exceeded`

**Solution:**
- Wait a few minutes before trying again
- Check your OpenAI account has available credits
- Upgrade to a paid plan if needed

---

## Next Steps

Once you have the MVP running:

1. **Experiment with different prompts** to see how the LLM interprets them
2. **Check the browser console** (F12) to see API requests/responses
3. **Review the code** to understand the architecture
4. **Try modifying** the DSL schema to add new primitive types
5. **Read the main README.md** for roadmap and contribution guidelines

---

## Architecture Overview

```
User Input (Web)
      ↓
API Gateway (:8000)
      ↓
   ┌──┴──┐
   ↓     ↓
LLM    Geometry
Orch.  Executor
(:8001) (:8002)
   ↓     ↓
  DSL → JSON
   ↓
Back to User
```

1. User enters a prompt in the web interface
2. API Gateway receives the request
3. LLM Orchestrator converts prompt to DSL using OpenAI
4. Geometry Executor processes the DSL (currently returns JSON)
5. Results sent back to the browser
6. Viewer displays the geometry

---

## File Structure Reference

```
promptcad/
├── apps/
│   ├── api-gateway/
│   │   ├── cmd/server/main.go          # Entry point
│   │   └── internal/handlers/          # HTTP handlers
│   └── viewer-web/
│       ├── src/
│       │   ├── pages/EditorPage.tsx    # Main UI
│       │   └── api/client.ts           # API client
│       └── package.json
├── services/
│   ├── llm-orchestrator/
│   │   ├── cmd/server/main.go          # Entry point
│   │   ├── internal/llm/client.go      # OpenAI integration
│   │   └── internal/prompt/parser.go   # Prompt parsing
│   └── geometry-exec/
│       ├── cmd/server/main.go          # Entry point
│       └── internal/primitives/        # Geometry generators
└── packages/
    └── dsl-schema/                     # Shared type definitions
```

---

## Support

For issues, questions, or suggestions:
1. Check this guide first
2. Review the main README.md
3. Check existing GitHub issues
4. Open a new issue with details

---

**You're now ready to use PromptCAD MVP!**
