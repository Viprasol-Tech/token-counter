"""
token-counter - Count tokens and calculate API costs

Part of Viprasol Utilities: https://viprasol.com
"""

__version__ = "0.1.0"
__author__ = "Viprasol"
__email__ = "hello@viprasol.com"
__url__ = "https://viprasol.com"

from .core import (
    CostCalculator,
    TokenCounter,
    calculate_cost,
    count_tokens,
    main,
    process,
)

__all__ = [
    "TokenCounter",
    "CostCalculator",
    "count_tokens",
    "calculate_cost",
    "main",
    "process",
]
