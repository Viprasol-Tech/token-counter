<div align="center">

<img src="docs/assets/logo.png" alt="Viprasol Tech logo" width="120" />

# token-counter

**Know what an LLM request will cost before you send it.**

_Built and maintained by [Viprasol Tech](https://viprasol.com) — Fintech Experts. Full-Stack Builders._

[![CI](https://img.shields.io/github/actions/workflow/status/Viprasol-Tech/token-counter/ci.yml?branch=master&style=flat-square&label=CI)](https://github.com/Viprasol-Tech/token-counter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-black?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen?style=flat-square)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=flat-square)](https://github.com/astral-sh/ruff)

</div>

---

`token-counter` estimates how many tokens a prompt will use and what the request will cost, using only the Python standard library. It is useful for budgets, rate-limit planning and quick sanity checks in scripts and CI. It needs no API key and no tokenizer download.

> **Estimates, not exact counts.** Most tokenizers average about 4 characters per English token, and `token-counter` uses per-model rates built on that (±25% on typical prose; code and non-English text vary more). When you need an exact number, use the provider's own token-counting endpoint.

## ✨ Features

- 🔢 **Token estimates** per model family (Claude, GPT, Gemini, Llama, Mistral).
- 💵 **Cost breakdowns** for input and output tokens, using per-model list prices.
- 📦 **Batch estimates** with total, average, min and max for a list of texts.
- 🛠️ **Bring your own prices:** add or override any model in one line.
- 🖥️ **CLI** (`token-counter`) and a small Python API.
- 🔒 Zero runtime dependencies; tested on Python 3.10–3.13.

## 🚀 Quickstart

```bash
git clone https://github.com/Viprasol-Tech/token-counter.git
cd token-counter
pip install -e .

token-counter "Summarise this contract in five bullet points." -m claude-3-haiku
token-counter "ignored" -i 12000 -o 800 -m gpt-4-turbo   # price known token counts
```

```text
Input tokens (estimated): 13
Output tokens: 500
Cost breakdown:
{
  "model": "claude-3-haiku",
  "input_tokens": 13,
  "output_tokens": 500,
  "total_tokens": 513,
  ...
}
```

## 🐍 Python API

```python
from token_counter import CostCalculator, TokenCounter, calculate_cost, count_tokens

count_tokens("Hello, world!", model="gpt-4")  # -> 3
TokenCounter.batch_estimate(["short", "a longer text"])  # totals, average, min, max

cost, details = CostCalculator.calculate_cost(10_000, 1_000, model="claude-3-sonnet")
calculate_cost(10_000, 1_000, model="gpt-4-turbo")  # -> 0.13 (USD)

# Prices change. Add or update the models you use (USD per 1M input/output tokens):
CostCalculator.PRICING["my-model"] = (1.00, 4.00)
TokenCounter.TOKEN_RATIOS["my-model"] = 270.0  # tokens per 1,000 characters
```

## ⚙️ CLI options

| Option | Meaning |
|---|---|
| `text` | Text to estimate |
| `-m, --model` | Model name; must be in the price table to get a cost |
| `-i, --input-tokens` | Use a known input token count instead of estimating |
| `-o, --output-tokens` | Expected output tokens (default 500) |

The built-in price table lists the published list prices for the model versions it names. Check your provider's pricing page and add current models with `CostCalculator.PRICING`.

## 🧪 Development

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check . && pytest
```

## 🤝 Contributing

PRs are welcome. Run `ruff check . && ruff format --check . && pytest` before you open one.

## 📬 Contact — Viprasol Tech Private Limited

- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech builds fintech software, algorithmic trading systems, MT4/MT5 bots, AI voice agents, and B2B SaaS. Need a custom build? [Get in touch](mailto:support@viprasol.com).*

## License

[MIT](LICENSE) © 2026 Viprasol Tech Private Limited
