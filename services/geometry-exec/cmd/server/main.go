package main

import (
	"log"
	"net/http"
	"promptcad/geometry-exec/internal/executor"
	
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	
	r.POST("/execute", func(c *gin.Context) {
		var dsl executor.DSL
		if err := c.ShouldBindJSON(&dsl); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		
		result, err := executor.Execute(dsl)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		
		c.JSON(http.StatusOK, gin.H{"geometry": result})
	})
	
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "healthy"})
	})
	
	log.Println("Geometry Executor running on :8002")
	r.Run(":8002")
}
