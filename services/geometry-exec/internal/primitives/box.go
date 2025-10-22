package primitives

import (
	"encoding/json"
	"fmt"
)

type BoxParams struct {
	Width  float64 `json:"width"`
	Height float64 `json:"height"`
	Depth  float64 `json:"depth"`
}

func GenerateBox(params map[string]interface{}) (string, error) {
	data, _ := json.Marshal(params)
	var p BoxParams
	if err := json.Unmarshal(data, &p); err != nil {
		return "", fmt.Errorf("invalid box params: %w", err)
	}
	
	result := fmt.Sprintf(`{"type":"box","width":%.2f,"height":%.2f,"depth":%.2f}`,
		p.Width, p.Height, p.Depth)
	return result, nil
}
