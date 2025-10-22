package llm

import (
	"context"
	"fmt"
	"os"
	openai "github.com/sashabaranov/go-openai"
)

type Client struct {
	client *openai.Client
}

func NewClient() *Client {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		panic("OPENAI_API_KEY environment variable not set")
	}
	return &Client{
		client: openai.NewClient(apiKey),
	}
}

func (c *Client) Complete(ctx context.Context, systemPrompt, userPrompt string) (string, error) {
	resp, err := c.client.CreateChatCompletion(ctx, openai.ChatCompletionRequest{
		Model: openai.GPT3Dot5Turbo,
		Messages: []openai.ChatCompletionMessage{
			{Role: openai.ChatMessageRoleSystem, Content: systemPrompt},
			{Role: openai.ChatMessageRoleUser, Content: userPrompt},
		},
		Temperature: 0.7,
	})
	if err != nil {
		return "", fmt.Errorf("openai completion failed: %w", err)
	}
	if len(resp.Choices) == 0 {
		return "", fmt.Errorf("no completion choices returned")
	}
	return resp.Choices[0].Message.Content, nil
}
