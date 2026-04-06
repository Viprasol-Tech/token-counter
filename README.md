# token-counter

> Know AI costs BEFORE sending requests. Count tokens for Claude, GPT, Gemini, and more.

Estimate token usage and calculate API costs instantly. No surprises on your bill.

**By [Viprasol](https://viprasol.com)**

## Features

- 🎯 **Support for all major models** - Claude, GPT-4, GPT-3.5, Gemini, Llama 2
- ⚡ **Instant estimation** - Get token counts in milliseconds
- 💰 **Cost calculation** - Know exact API costs before making calls
- 📊 **Batch processing** - Analyze multiple texts at once
- 🔧 **Simple API** - Works with Python or CLI
- 📦 **Zero dependencies** - Uses only Python standard library

## Installation

```bash
pip install token-counter
```

## Quick Start

```python
from token_counter import count_tokens, calculate_cost

# Count tokens
tokens = count_tokens("Your text here")
print(f"Tokens: {tokens}")

# Calculate cost
cost = calculate_cost(input_tokens=1000, output_tokens=500, model="gpt-4-turbo")
print(f"Cost: ${cost:.4f}")
```

## Usage Examples

### Example 1: Count Tokens

```python
from token_counter import count_tokens

text = "This is the text I want to send to an AI model"
tokens = count_tokens(text, model="claude-3-opus")
print(f"This text uses approximately {tokens} tokens")
```

### Example 2: Estimate Request Cost

```python
from token_counter import CostCalculator

prompt = "Analyze this large document..."
result = CostCalculator.estimate_request_cost(
    prompt=prompt,
    expected_output_tokens=1000,
    model="gpt-4-turbo"
)

print(f"Input cost: ${result['input_cost']:.6f}")
print(f"Output cost: ${result['output_cost']:.6f}")  
print(f"Total: ${result['total_cost']:.6f}")
```

### Example 3: Batch Analysis

```python
from token_counter import TokenCounter

texts = [
    "Short prompt",
    "This is a medium length prompt with more text",
    "This is a very long prompt..." * 100
]

result = TokenCounter.batch_estimate(texts, model="claude-3-sonnet")
print(f"Total tokens: {result['total']}")
print(f"Average: {result['average']}")
print(f"Range: {result['min']} - {result['max']}")
```

### Example 4: CLI Usage

```bash
# Count tokens
token-counter "Your text here"

# Specific model
token-counter "Your text" --model gpt-4

# Estimate cost (assumes 500 output tokens)
token-counter "Your text" -c 500 --model gpt-4-turbo

# Full cost calculation
token-counter "Your text" -i 1000 -o 500 --model claude-3-opus
```

## Supported Models

| Model | Input Price | Output Price | Use Case |
|-------|-------------|--------------|----------|
| claude-3-opus | $15/1M | $75/1M | Most capable |
| claude-3-sonnet | $3/1M | $15/1M | Balanced |
| claude-3-haiku | $0.25/1M | $1.25/1M | Fast & cheap |
| gpt-4 | $30/1M | $60/1M | Most expensive |
| gpt-4-turbo | $10/1M | $30/1M | Good value |
| gpt-3.5-turbo | $0.50/1M | $1.50/1M | Budget |
| gemini-pro | $0.50/1M | $1.50/1M | Free alternative |

## API Reference

### `count_tokens(text, model="default") -> int`

Estimate token count for text.

```python
tokens = count_tokens("Hello world", model="gpt-4")
```

### `TokenCounter.estimate_tokens(text, model, include_overhead=False) -> int`

Advanced token counting with overhead option.

```python
tokens = TokenCounter.estimate_tokens(text, model="claude-3-opus", include_overhead=True)
```

### `TokenCounter.batch_estimate(texts, model) -> dict`

Analyze multiple texts at once.

```python
result = TokenCounter.batch_estimate(["text1", "text2"], model="gpt-4-turbo")
# Returns: {'total': X, 'average': X, 'min': X, 'max': X, ...}
```

### `CostCalculator.calculate_cost(input_tokens, output_tokens, model) -> (float, dict)`

Calculate exact API cost.

```python
cost, details = CostCalculator.calculate_cost(1000, 500, model="gpt-4-turbo")
```

### `CostCalculator.estimate_request_cost(prompt, expected_output_tokens, model) -> dict`

Estimate cost for complete request.

```python
result = CostCalculator.estimate_request_cost(
    prompt="Your prompt...",
    expected_output_tokens=500,
    model="claude-3-opus"
)
```

## Real-World Examples

### Budget Planning

```python
from token_counter import CostCalculator

documents = [doc1, doc2, doc3]  # Large documents to analyze
total_cost = 0

for doc in documents:
    result = CostCalculator.estimate_request_cost(
        doc,
        expected_output_tokens=200,
        model="gpt-4-turbo"
    )
    total_cost += result['total_cost']

print(f"Estimated cost to process all documents: ${total_cost:.2f}")
```

### Model Comparison

```python
from token_counter import CostCalculator

prompt = "Your prompt here..."

for model in ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]:
    result = CostCalculator.estimate_request_cost(prompt, 500, model=model)
    print(f"{model}: ${result['total_cost']:.6f}")
```

### Batch Cost Analysis

```python
from token_counter import TokenCounter

texts = ["batch", "of", "prompts"]
result = TokenCounter.batch_estimate(texts, model="claude-3-sonnet")

print(f"Total to process: ${(result['total'] * 3 / 1_000_000):.6f}")
```

## How It Works

Token counting uses character-based estimation with model-specific ratios:

- **Claude 3 Opus**: ~6 tokens per 1000 characters
- **Claude 3 Sonnet**: ~5.5 tokens per 1000 characters
- **GPT-4**: ~4 tokens per 1000 characters
- **GPT-3.5**: ~4 tokens per 1000 characters

These ratios provide accurate estimates for budget planning. For exact counts before submission, use the model's official tokenizer.

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=token_counter
```

**22 test cases** covering:
- Token estimation for all models
- Cost calculations and pricing
- Batch processing
- Edge cases and unicode handling

## Why This Matters

🎯 **No Surprises** - Calculate costs before sending expensive requests  
💰 **Budget Control** - Track spending across multiple models  
📊 **Optimization** - Find cost-efficient models for your use case  
⚡ **Planning** - Estimate time and costs for large batch jobs  

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT - see [LICENSE](LICENSE)

## Support

- **Website:** [viprasol.com](https://viprasol.com)
- **Email:** [hello@viprasol.com](mailto:hello@viprasol.com)
- **Issues:** [GitHub Issues](https://github.com/viprasol/token-counter/issues)

---

**Made by [Viprasol](https://viprasol.com) for AI efficiency.**
