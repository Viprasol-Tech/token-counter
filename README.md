# Token Counter

Count tokens and calculate API costs across multiple LLM models

## Features

- Zero external dependencies (stdlib only)
- Easy-to-use CLI interface
- Professional Python implementation
- MIT licensed

## Installation

```bash
pip install -e .
```

Or clone and install:

```bash
git clone https://github.com/Viprasol-Tech/token-counter
cd token-counter
pip install -e .
```

## Usage

### Python

```python
from token_counter import TokenCounter

result = TokenCounter.process("data")
print(result)
```

### CLI

```bash
python -m token_counter "your input here"
```

## Documentation

See the source code and docstrings for detailed API documentation.

## License

MIT License - see LICENSE file for details

## About

Part of Viprasol Utilities: https://viprasol.com

Created by Viprasol - Building AI-focused tools for developers.
