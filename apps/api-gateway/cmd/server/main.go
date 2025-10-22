package main

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
