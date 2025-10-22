import os
import json

# Define all file contents
files = {
    "services/geometry-exec/internal/primitives/box.go": '''package primitives

import (
	"encoding/json"
	"fmt"
)

type BoxParams struct {
	Width  float64 `+"`json:\"width\"`"+`
	Height float64 `+"`json:\"height\"`"+`
	Depth  float64 `+"`json:\"depth\"`"+`
}

func GenerateBox(params map[string]interface{}) (string, error) {
	data, _ := json.Marshal(params)
	var p BoxParams
	if err := json.Unmarshal(data, &p); err != nil {
		return "", fmt.Errorf("invalid box params: %w", err)
	}
	
	return `+"`{\"type\":\"box\",\"width\":`"+`+fmt.Sprintf(\"%.2f\",p.Width)+`+"`," + `
		`+"`\"height\":`"+`+fmt.Sprintf(\"%.2f\",p.Height)+`+"`," + `
		`+"`\"depth\":`"+`+fmt.Sprintf(\"%.2f\",p.Depth)+`+"`}`"+`, nil
}
''',

    "services/geometry-exec/internal/executor/executor.go": '''package executor

import (
	"fmt"
	"promptcad/geometry-exec/internal/primitives"
)

type Operation struct {
	ID     string                 `+"`json:\"id\"`"+`
	Type   string                 `+"`json:\"type\"`"+`
	Params map[string]interface{} `+"`json:\"params\"`"+`
	Inputs []string               `+"`json:\"inputs\"`"+`
}

type DSL struct {
	Version    string      `+"`json:\"version\"`"+`
	Operations []Operation `+"`json:\"operations\"`"+`
}

func Execute(dsl DSL) (string, error) {
	results := make(map[string]string)
	
	for _, op := range dsl.Operations {
		switch op.Type {
		case "box":
			result, err := primitives.GenerateBox(op.Params)
			if err != nil {
				return "", err
			}
			results[op.ID] = result
		default:
			return "", fmt.Errorf("unsupported operation: %s", op.Type)
		}
	}
	
	return results[dsl.Operations[len(dsl.Operations)-1].ID], nil
}
''',

    "services/geometry-exec/cmd/server/main.go": '''package main

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
''',
}

# Create all files
base_path = r"C:\Users\baris\Downloads\promptcad"
for file_path, content in files.items():
    full_path = os.path.join(base_path, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {file_path}")

print("\nAll files created successfully!")
