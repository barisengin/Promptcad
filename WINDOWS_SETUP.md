# Windows Setup Guide - PromptCAD MVP

## Prerequisites

### 1. Install Go
- Download: https://go.dev/dl/
- Get: `go1.21.x.windows-amd64.msi`
- Run installer
- Verify: Open CMD and run `go version`

### 2. Install Node.js
- Download: https://nodejs.org/
- Get: LTS version (18.x or higher)
- Run installer (include npm)
- Verify: Open CMD and run `node --version` and `npm --version`

### 3. Get OpenAI API Key
- Visit: https://platform.openai.com/api-keys
- Sign up/Login
- Click "Create new secret key"
- Copy the key (starts with `sk-`)

---

## Installation Steps

### Step 1: Configure Environment

```bash
# Open Command Prompt in project folder
cd C:\Users\baris\Downloads\promptcad

# Copy environment template
copy .env.example .env

# Edit .env file
notepad .env
```

In Notepad, replace `your-openai-api-key-here` with your actual key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

Save and close Notepad.

### Step 2: Install Dependencies

```bash
# Run the Windows installer
install.bat
```

This will:
1. Install npm packages for viewer-web
2. Install npm packages for dsl-schema
3. Download Go modules for llm-orchestrator
4. Download Go modules for geometry-exec
5. Download Go modules for api-gateway

**Expected output:**
```
================================================
PromptCAD MVP - Installing Dependencies
================================================

[1/5] Installing viewer-web dependencies...
Done: viewer-web dependencies installed

[2/5] Installing dsl-schema dependencies...
Done: dsl-schema dependencies installed

[3/5] Downloading llm-orchestrator Go modules...
Done: llm-orchestrator modules downloaded

[4/5] Downloading geometry-exec Go modules...
Done: geometry-exec modules downloaded

[5/5] Downloading api-gateway Go modules...
Done: api-gateway modules downloaded

================================================
Installation Complete!
================================================
```

---

## Running the Application

### Start All Services

```bash
# From project root
scripts\start-dev.bat
```

This will open **4 command prompt windows**:
1. **LLM Orchestrator** - Port 8001
2. **Geometry Executor** - Port 8002
3. **API Gateway** - Port 8000
4. **Viewer Web** - Port 5173

**Wait for all services to show "running" messages.**

### Access the Application

Open your browser to: **http://localhost:5173**

---

## Testing

### 1. Health Checks

Open a new Command Prompt and test each service:

```bash
# Test LLM Orchestrator
curl http://localhost:8001/health

# Test Geometry Executor
curl http://localhost:8002/health

# Test API Gateway
curl http://localhost:8000/api/health
```

Each should return: `{"status":"healthy"}`

**Note:** If `curl` is not recognized, use PowerShell instead or test directly in browser.

### 2. Test Full Pipeline

```bash
curl -X POST http://localhost:8000/api/prompt -H "Content-Type: application/json" -d "{\"prompt\": \"Create a box 100mm wide, 50mm tall, 30mm deep\"}"
```

### 3. Test Web Interface

1. Go to: http://localhost:5173
2. You should see:
   - Left panel: Prompt input area
   - Right panel: 3D viewer with grid
3. Enter: "Create a box 100mm wide, 50mm tall, 30mm deep"
4. Click "Generate Model"
5. Wait 5-10 seconds
6. See geometry JSON in left panel

---

## Common Windows Issues

### Issue: "go is not recognized"

**Solution:**
1. Reinstall Go from https://go.dev/dl/
2. During install, check "Add to PATH"
3. Close and reopen Command Prompt
4. Try `go version` again

### Issue: "node is not recognized"

**Solution:**
1. Reinstall Node.js from https://nodejs.org/
2. Use default installation options
3. Close and reopen Command Prompt
4. Try `node --version` again

### Issue: Port Already in Use

**Error:** `listen tcp :8000: bind: Only one usage of each socket address`

**Solution:**
```bash
# Find what's using the port
netstat -ano | findstr :8000

# Kill the process (replace 1234 with PID from above)
taskkill /PID 1234 /F
```

### Issue: npm Install Fails

**Solution:**
```bash
cd apps\viewer-web
rmdir /s /q node_modules
del package-lock.json
npm cache clean --force
npm install
cd ..\..
```

### Issue: OPENAI_API_KEY Not Found

**Solution:**
1. Check `.env` file exists (not `.env.example`)
2. Open `.env` in Notepad
3. Ensure key starts with `sk-`
4. No quotes around the key
5. Save file
6. Restart all service windows

### Issue: Services Won't Start

**Solution:**
1. Check Windows Firewall isn't blocking ports
2. Run Command Prompt as Administrator
3. Close any VPN or proxy software
4. Restart computer and try again

---

## Stopping the Services

To stop all services:
1. Close each of the 4 Command Prompt windows
2. Or press `Ctrl+C` in each window

---

## File Locations

**Configuration:**
- Environment: `C:\Users\baris\Downloads\promptcad\.env`

**Services:**
- LLM Orchestrator: `services\llm-orchestrator\`
- Geometry Executor: `services\geometry-exec\`
- API Gateway: `apps\api-gateway\`
- Viewer Web: `apps\viewer-web\`

**Scripts:**
- Install: `install.bat`
- Start: `scripts\start-dev.bat`

**Documentation:**
- Quick start: `START_HERE.md`
- This guide: `WINDOWS_SETUP.md`
- Full docs: `README.md`
- Troubleshooting: `SETUP.md`

---

## Next Steps

1. ✅ Install prerequisites (Go, Node.js)
2. ✅ Configure .env with OpenAI key
3. ✅ Run `install.bat`
4. ✅ Run `scripts\start-dev.bat`
5. ✅ Access http://localhost:5173
6. ✅ Test with example prompts
7. 📖 Read documentation
8. 💻 Explore the code

---

## Support

**Still having issues?**
1. Check all prerequisites are installed
2. Verify .env file has correct API key
3. Read SETUP.md for detailed troubleshooting
4. Check service logs in Command Prompt windows

---

**You're ready to go! 🚀**
