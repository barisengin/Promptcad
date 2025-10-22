package prompt

import (
	"context"
	"encoding/json"
	"fmt"
	"promptcad/llm-orchestrator/internal/llm"
	"strings"
)

type Parser struct {
	llmClient *llm.Client
}

func NewParser(llmClient *llm.Client) *Parser {
	return &Parser{llmClient: llmClient}
}

func (p *Parser) ParseToDSL(ctx context.Context, userPrompt string) (map[string]interface{}, error) {
	response, err := p.llmClient.Complete(ctx, llm.SystemPrompt, userPrompt)
	if err != nil {
		return nil, fmt.Errorf("llm completion failed: %w", err)
	}
	
	cleaned := strings.TrimSpace(response)
	cleaned = strings.Trim(cleaned, "`")
	if strings.HasPrefix(cleaned, "json") {
		cleaned = strings.TrimPrefix(cleaned, "json")
		cleaned = strings.TrimSpace(cleaned)
	}
	
	var dsl map[string]interface{}
	if err := json.Unmarshal([]byte(cleaned), &dsl); err != nil {
		return nil, fmt.Errorf("failed to parse DSL JSON: %w", err)
	}
	
	return dsl, nil
}
