package executor

import (
	"fmt"
	"promptcad/geometry-exec/internal/primitives"
)

type Operation struct {
	ID     string                 `json:"id"`
	Type   string                 `json:"type"`
	Params map[string]interface{} `json:"params"`
	Inputs []string               `json:"inputs"`
}

type DSL struct {
	Version    string      `json:"version"`
	Operations []Operation `json:"operations"`
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
	
	if len(dsl.Operations) == 0 {
		return "", fmt.Errorf("no operations in DSL")
	}
	
	return results[dsl.Operations[len(dsl.Operations)-1].ID], nil
}
