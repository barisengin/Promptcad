package handlers

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
	Prompt string `json:"prompt"`
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

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("llm service returned status %d: %s", resp.StatusCode, string(body))
	}

	var dsl map[string]interface{}
	if err := json.Unmarshal(body, &dsl); err != nil {
		return nil, fmt.Errorf("failed to parse LLM response: %w", err)
	}
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

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("geometry service returned status %d: %s", resp.StatusCode, string(body))
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("failed to parse geometry response: %w", err)
	}
	return result["geometry"], nil
}
