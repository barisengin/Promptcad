# 🚀 START HERE - PromptCAD MVP

## What is This?

An **AI-powered CAD system** that converts natural language to 3D models.

Example: "Create a box 100mm wide, 50mm tall, 30mm deep" → 3D geometry

---

## 3-Minute Setup

### 1️⃣ Prerequisites

```bash
# Check you have these installed:
go version    # Need 1.21+
node --version # Need v18+
```

Don't have them? Download:
- Go: https://go.dev/dl/
- Node.js: https://nodejs.org/

Get OpenAI API key: https://platform.openai.com/api-keys

### 2️⃣ Configure

```bash
# Copy environment file
cp .env.example .env

# Edit .env and add your OpenAI key:
# OPENAI_API_KEY=sk-your-key-here
```

### 3️⃣ Install

**Windows:**
```bash
install.bat
```

**Linux/Mac (with make):**
```bash
make install
```

### 4️⃣ Run

**Windows:**
```bash
scripts\start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/start-dev.sh
./scripts/start-dev.sh
```

### 5️⃣ Access

Open browser: **http://localhost:5173**

Enter prompt: "Create a box 100mm wide, 50mm tall, 30mm deep"

Click "Generate Model" → See result!

---

## Architecture

```
┌─────────────┐
│   Browser   │ :5173
│ React+Three │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ API Gateway │ :8000
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
┌─────┐ ┌─────────┐
│ LLM │ │Geometry │
│:8001│ │  :8002  │
└─────┘ └─────────┘
```

---

## Documentation

- **START_HERE.md** ← You are here
- **SETUP.md** - Detailed setup & troubleshooting
- **README.md** - Complete documentation
- **EXECUTION_CHECKLIST.md** - Step-by-step verification
- **MVP_IMPLEMENTATION_SUMMARY.md** - Technical details

---

## Quick Test

```bash
# Test the full system:
curl -X POST http://localhost:8000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a box 100mm wide, 50mm tall, 30mm deep"}'
```

---

## Troubleshooting

**Services won't start?**
- Check OPENAI_API_KEY in .env file
- Make sure ports 5173, 8000, 8001, 8002 are free

**"Module not found" errors?**
- Run: `install.bat` again (Windows) or `make install` (Linux/Mac)
- Check internet connection

**Need help?**
- Read SETUP.md for detailed troubleshooting
- Check service logs in terminal windows

---

## What's Implemented

✅ Natural language prompt input
✅ OpenAI LLM integration  
✅ DSL generation
✅ Mock geometry execution
✅ 3D web viewer
✅ End-to-end workflow

## What's Not (Yet)

❌ Real 3D mesh generation (returns JSON)
❌ Multiple primitives (only box works)
❌ Boolean operations
❌ Database persistence
❌ File export (STEP/STL)

These are planned for Phase 2.

---

## Project Structure

```
promptcad/
├── apps/
│   ├── api-gateway/      # Go REST API
│   └── viewer-web/       # React frontend
├── services/
│   ├── llm-orchestrator/ # OpenAI integration
│   └── geometry-exec/    # Geometry engine
├── packages/
│   └── dsl-schema/       # Shared types
└── scripts/
    └── start-dev.*       # Startup scripts
```

---

## Next Steps

1. ✅ Follow the 5-step setup above
2. ✅ Verify services are running (check terminals)
3. ✅ Test the web interface
4. 📖 Read SETUP.md for details
5. 🚀 Experiment with prompts
6. 💻 Explore the code

---

**Questions?** Check SETUP.md or README.md for answers.

**Ready to build?** All code follows a strict 75-line limit per file for maintainability.

**Status:** MVP Complete ✅ - Ready to run!
