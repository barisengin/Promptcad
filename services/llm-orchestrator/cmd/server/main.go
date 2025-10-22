package main

import (
	"log"
	"net/http"
	"promptcad/llm-orchestrator/internal/llm"
	"promptcad/llm-orchestrator/internal/prompt"
	
	"github.com/gin-gonic/gin"
)

type PromptRequest struct {
	Prompt string `json:"prompt" binding:"required"`
}

func main() {
	llmClient := llm.NewClient()
	parser := prompt.NewParser(llmClient)
	
	r := gin.Default()
	
	r.POST("/parse", func(c *gin.Context) {
		var req PromptRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			log.Printf("ERROR: Bad request: %v", err)
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		log.Printf("Processing prompt: %s", req.Prompt)

		dsl, err := parser.ParseToDSL(c.Request.Context(), req.Prompt)
		if err != nil {
			log.Printf("ERROR: Failed to parse prompt: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		log.Printf("Successfully generated DSL")
		c.JSON(http.StatusOK, dsl)
	})
	
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "healthy"})
	})
	
	log.Println("LLM Orchestrator running on :8001")
	r.Run(":8001")
}
