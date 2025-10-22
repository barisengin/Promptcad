# PromptCAD MVP

**AI-Powered, Cloud-Native CAD System** - Convert natural language prompts into parametric 3D models.

## Overview

PromptCAD is a microservices-based CAD platform that uses Large Language Models (LLMs) to translate natural language descriptions into 3D geometry. This MVP demonstrates the core concept with a simplified architecture.

### Architecture

```
┌─────────────┐
│   Browser   │
│  (React +   │
│  Three.js)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ API Gateway │ :8000
│    (Go)     │
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│LLM Orch.    │   │  Geometry   │
│  (Go +      │   │  Executor   │
│  OpenAI)    │   │    (Go)     │
│   :8001     │   │   :8002     │
└─────────────┘   └─────────────┘
```

## What's Implemented (MVP Scope)

✅ **DSL Schema Package**: JSON schema for CAD primitives  
✅ **LLM Orchestrator**: OpenAI integration for prompt → DSL conversion  
✅ **Geometry Executor**: Mock geometry generation (returns JSON)  
✅ **API Gateway**: REST API orchestrating all services  
✅ **Viewer Web**: React + Three.js 3D viewer  
✅ **Development Scripts**: One-command startup for all services  

## Prerequisites

- **Go 1.21+** ([Download](https://go.dev/dl/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **OpenAI API Key** ([Get one](https://platform.openai.com/api-keys))

## Quick Start

### 1. Clone & Setup

```bash
cd promptcad

# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

### 2. Install Dependencies

```bash
make install
```

This will:
- Install npm packages for viewer-web and dsl-schema
- Download Go modules for all services

### 3. Start All Services

**On Windows:**
```bash
scripts\start-dev.bat
```

**On Linux/Mac:**
```bash
chmod +x scripts/start-dev.sh
./scripts/start-dev.sh
```

### 4. Access the Application

Open your browser to: **http://localhost:5173**

## Usage

1. Enter a natural language prompt in the text area:
   ```
   Create a box 100mm wide, 50mm tall, and 30mm deep
   ```

2. Click "Generate Model"

3. The system will:
   - Send prompt to LLM Orchestrator (converts to DSL)
   - Execute DSL in Geometry Executor (generates geometry)
   - Display result in the 3D viewer

## Supported Prompts (MVP)

The MVP supports basic primitives:

- **Box**: "Create a box 10mm wide, 20mm tall, 5mm deep"
- **Cylinder**: "Make a cylinder with radius 5mm and height 15mm"
- **Sphere**: "Generate a sphere with radius 8mm"

## Project Structure

```
promptcad/
├── apps/
│   ├── api-gateway/           # REST API gateway (Go)
│   └── viewer-web/            # React + Three.js viewer
├── services/
│   ├── llm-orchestrator/      # OpenAI prompt→DSL service
│   └── geometry-exec/         # Geometry generation service
├── packages/
│   └── dsl-schema/            # Shared DSL type definitions
├── scripts/
│   ├── start-dev.sh           # Linux/Mac startup script
│   └── start-dev.bat          # Windows startup script
├── .env.example               # Environment template
├── Makefile                   # Build commands
└── README.md                  # This file
```

## Development

### Running Individual Services

**LLM Orchestrator:**
```bash
cd services/llm-orchestrator
OPENAI_API_KEY=sk-... go run cmd/server/main.go
```

**Geometry Executor:**
```bash
cd services/geometry-exec
go run cmd/server/main.go
```

**API Gateway:**
```bash
cd apps/api-gateway
go run cmd/server/main.go
```

**Viewer Web:**
```bash
cd apps/viewer-web
npm run dev
```

### Service Endpoints

- **Viewer Web**: http://localhost:5173
- **API Gateway**: http://localhost:8000
  - `POST /api/prompt` - Process natural language prompt
  - `GET /api/health` - Health check
- **LLM Orchestrator**: http://localhost:8001
  - `POST /parse` - Parse prompt to DSL
  - `GET /health` - Health check
- **Geometry Executor**: http://localhost:8002
  - `POST /execute` - Execute DSL to geometry
  - `GET /health` - Health check

## Testing the Services

### Test LLM Orchestrator
```bash
curl -X POST http://localhost:8001/parse \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a box 10mm wide, 20mm tall, 5mm deep"}'
```

### Test Geometry Executor
```bash
curl -X POST http://localhost:8002/execute \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.0",
    "operations": [
      {
        "id": "box1",
        "type": "box",
        "params": {"width": 10, "height": 20, "depth": 5}
      }
    ]
  }'
```

### Test Full Pipeline
```bash
curl -X POST http://localhost:8000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a box 10mm wide, 20mm tall, 5mm deep"}'
```

## Known Limitations (MVP)

1. **No Real Geometry**: The geometry executor returns JSON, not actual 3D meshes (no OpenCASCADE integration yet)
2. **Limited Operations**: Only box primitive is fully implemented
3. **No Persistence**: No database; all data is in-memory
4. **No Assembly Support**: Single-part models only
5. **No Export**: Can't export STEP/STL files yet
6. **Basic Viewer**: Simple box rendering; no advanced materials or LOD

## Roadmap (Post-MVP)

### Phase 2 - Real Geometry
- [ ] Integrate OpenCASCADE (C++)
- [ ] Implement cylinder, sphere primitives
- [ ] Add boolean operations (union, subtract)
- [ ] Implement fillets and chamfers
- [ ] Generate actual glTF meshes

### Phase 3 - Advanced Features
- [ ] PostgreSQL database integration
- [ ] Assembly support with constraints
- [ ] Export to STEP/STL/glTF
- [ ] Parametric dimensions with editing
- [ ] Material library

### Phase 4 - Production Ready
- [ ] Kubernetes deployment
- [ ] Authentication & authorization
- [ ] Multi-user collaboration
- [ ] Version control (PDM service)
- [ ] Performance optimization (LOD, caching)

## Troubleshooting

### "OPENAI_API_KEY not set"
- Make sure you've copied `.env.example` to `.env`
- Add your OpenAI API key to `.env`

### Port Already in Use
- Check if another service is using ports 5173, 8000, 8001, or 8002
- Kill the process: `lsof -ti:8000 | xargs kill` (Mac/Linux)

### Go Dependencies Not Found
```bash
cd services/llm-orchestrator && go mod tidy
cd services/geometry-exec && go mod tidy
cd apps/api-gateway && go mod tidy
```

### npm Install Fails
```bash
cd apps/viewer-web
rm -rf node_modules package-lock.json
npm install
```

## Architecture Decisions

### Why Microservices?
Each service has different performance characteristics:
- LLM calls are I/O-bound
- Geometry computation is CPU-bound
- Viewer is latency-sensitive

This allows independent scaling and technology choices.

### Why Go for Backend?
- Fast compilation and execution
- Excellent concurrency support (goroutines)
- Small deployment footprint
- Strong HTTP/gRPC libraries

### Why React + Three.js?
- Industry standard for 3D web rendering
- Large ecosystem of CAD visualization tools
- Real-time interaction capabilities

## Contributing

This is an MVP demonstrating the architecture. Future contributions should:
1. Follow the 75-line-per-file constraint
2. Add tests for new functionality
3. Update documentation
4. Follow existing code structure

## License

See LICENSE file for details.

## Contact & Support

For issues or questions, please open an issue on the repository.

---

**Built with ❤️ to demonstrate AI-powered CAD concepts**
