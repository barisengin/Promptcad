# PromptCAD MVP Makefile

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
