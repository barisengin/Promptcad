import os

files = {
    "apps/api-gateway/go.mod": '''module promptcad/api-gateway

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	github.com/gin-contrib/cors v1.5.0
)
''',

    "apps/api-gateway/cmd/server/main.go": '''package main

import (
	"log"
	"promptcad/api-gateway/internal/handlers"
	
	"github.com/gin-gonic/gin"
	"github.com/gin-contrib/cors"
)

func main() {
	r := gin.Default()
	
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		AllowCredentials: true,
	}))
	
	promptHandler := handlers.NewPromptHandler()
	
	r.POST("/api/prompt", promptHandler.ProcessPrompt)
	r.GET("/api/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "healthy"})
	})
	
	log.Println("API Gateway running on :8000")
	r.Run(":8000")
}
''',

    "apps/api-gateway/internal/handlers/prompt_handler.go": '''package handlers

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	
	"github.com/gin-gonic/gin"
)

type PromptHandler struct {
	llmURL      string
	geometryURL string
}

func NewPromptHandler() *PromptHandler {
	return &PromptHandler{
		llmURL:      "http://localhost:8001",
		geometryURL: "http://localhost:8002",
	}
}

type PromptRequest struct {
	Prompt string `'''+"json:\"prompt\""+'''`
}

func (h *PromptHandler) ProcessPrompt(c *gin.Context) {
	var req PromptRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	dsl, err := h.callLLMOrchestrator(req.Prompt)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	geometry, err := h.callGeometryExecutor(dsl)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"dsl":      dsl,
		"geometry": geometry,
	})
}

func (h *PromptHandler) callLLMOrchestrator(prompt string) (map[string]interface{}, error) {
	payload := map[string]string{"prompt": prompt}
	data, _ := json.Marshal(payload)
	
	resp, err := http.Post(h.llmURL+"/parse", "application/json", bytes.NewBuffer(data))
	if err != nil {
		return nil, fmt.Errorf("llm service error: %w", err)
	}
	defer resp.Body.Close()
	
	body, _ := io.ReadAll(resp.Body)
	var dsl map[string]interface{}
	json.Unmarshal(body, &dsl)
	return dsl, nil
}

func (h *PromptHandler) callGeometryExecutor(dsl map[string]interface{}) (interface{}, error) {
	data, _ := json.Marshal(dsl)
	
	resp, err := http.Post(h.geometryURL+"/execute", "application/json", bytes.NewBuffer(data))
	if err != nil {
		return nil, fmt.Errorf("geometry service error: %w", err)
	}
	defer resp.Body.Close()
	
	body, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	json.Unmarshal(body, &result)
	return result["geometry"], nil
}
''',
}

base_path = r"C:\Users\baris\Downloads\promptcad"
for file_path, content in files.items():
    full_path = os.path.join(base_path, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {file_path}")

print("\nAPI Gateway created successfully!")
