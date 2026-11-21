"""
Token counter for AI models.

Estimate token usage for Claude, OpenAI, Gemini, and other models.
Know costs BEFORE sending requests to APIs.
"""


class TokenCounter:
    """Count tokens for different AI models."""

    # Approximate tokens per 1,000 characters of English text. Most tokenizers
    # average about 4 characters per token (~250 per 1,000); Claude's runs
    # slightly denser. Treat results as +/-25% estimates, and use the
    # provider's token-counting endpoint when you need an exact number.
    TOKEN_RATIOS = {
        "claude-3-opus": 285.0,
        "claude-3-sonnet": 285.0,
        "claude-3-haiku": 285.0,
        "gpt-4": 250.0,
        "gpt-4-turbo": 250.0,
        "gpt-3.5-turbo": 250.0,
        "gemini-pro": 250.0,
        "gemini-pro-vision": 250.0,
        "llama-2": 270.0,
        "mistral": 270.0,
        "default": 270.0,
    }

    @staticmethod
    def count_characters(text: str) -> int:
        """Count characters in text."""
        if not isinstance(text, str):
            text = str(text)
        return len(text)

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text."""
        if not isinstance(text, str):
            text = str(text)
        return len(text.split())

    @staticmethod
    def count_lines(text: str) -> int:
        """Count lines in text."""
        if not isinstance(text, str):
            text = str(text)
        return len(text.split("\n"))

    @classmethod
    def estimate_tokens(
        cls,
        text: str,
        model: str = "default",
        include_overhead: bool = False,
    ) -> int:
        """
        Estimate token count for text.

        Uses character-based estimation with model-specific ratios.

        Args:
            text: Input text to count
            model: Model name (claude-3-opus, gpt-4, etc.)
            include_overhead: Add 10% overhead for safety

        Returns:
            Estimated token count

        Examples:
            >>> counter = TokenCounter()
            >>> tokens = counter.estimate_tokens("Hello world", model="claude-3-opus")
            >>> tokens > 0
            True
        """
        char_count = cls.count_characters(text)
        ratio = cls.TOKEN_RATIOS.get(model.lower(), cls.TOKEN_RATIOS["default"])

        if char_count == 0:
            return 1
        estimated = round(char_count / 1000 * ratio)

        if include_overhead:
            estimated = int(estimated * 1.1)  # Add 10% buffer

        return max(1, estimated)

    @classmethod
    def batch_estimate(
        cls,
        texts: list,
        model: str = "default",
    ) -> dict[str, int]:
        """
        Estimate tokens for multiple texts.

        Args:
            texts: List of texts
            model: Model name

        Returns:
            Dict with total and per-item counts

        Examples:
            >>> texts = ["Hello", "World", "Test"]
            >>> result = TokenCounter.batch_estimate(texts)
            >>> "total" in result
            True
        """
        results = {
            "texts": len(texts),
            "total": 0,
            "average": 0,
            "min": float("inf"),
            "max": 0,
            "details": [],
        }

        for text in texts:
            tokens = cls.estimate_tokens(text, model=model)
            results["total"] += tokens
            results["min"] = min(results["min"], tokens)
            results["max"] = max(results["max"], tokens)
            results["details"].append({"text": text[:50], "tokens": tokens})

        if texts:
            results["average"] = results["total"] // len(texts)

        if results["min"] == float("inf"):
            results["min"] = 0

        return results


class CostCalculator:
    """Calculate API costs based on token usage."""

    # List prices in USD per 1M tokens (input, output) for these model versions.
    # Prices change: add or update entries for the models you use, e.g.
    # CostCalculator.PRICING["my-model"] = (1.0, 4.0)
    PRICING = {
        "claude-3-opus": (15.0, 75.0),
        "claude-3-sonnet": (3.0, 15.0),
        "claude-3-haiku": (0.25, 1.25),
        "gpt-4": (30.0, 60.0),
        "gpt-4-turbo": (10.0, 30.0),
        "gpt-3.5-turbo": (0.50, 1.50),
        "gemini-pro": (0.50, 1.50),
    }

    @classmethod
    def calculate_cost(
        cls,
        input_tokens: int,
        output_tokens: int,
        model: str = "gpt-3.5-turbo",
    ) -> tuple[float, dict]:
        """
        Calculate API cost for token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model name

        Returns:
            Tuple of (total_cost, details_dict)

        Examples:
            >>> cost, details = CostCalculator.calculate_cost(1000, 500, model="gpt-4-turbo")
            >>> cost > 0
            True
        """
        if model not in cls.PRICING:
            raise ValueError(f"Unknown model: {model}")

        input_price, output_price = cls.PRICING[model]

        # Calculate costs
        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price
        total_cost = input_cost + output_cost

        return total_cost, {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6),
            "input_price_per_1m": input_price,
            "output_price_per_1m": output_price,
        }

    @classmethod
    def estimate_request_cost(
        cls,
        prompt: str,
        expected_output_tokens: int = 500,
        model: str = "gpt-3.5-turbo",
    ) -> dict:
        """
        Estimate cost for a complete request.

        Args:
            prompt: Input prompt
            expected_output_tokens: Estimated output token count
            model: Model name

        Returns:
            Cost breakdown
        """
        input_tokens = TokenCounter.estimate_tokens(prompt, model=model)
        cost, details = cls.calculate_cost(input_tokens, expected_output_tokens, model=model)
        return details


def count_tokens(text: str, model: str = "default") -> int:
    """
    Quick token counter.

    Args:
        text: Text to count
        model: Model name

    Returns:
        Estimated token count
    """
    return TokenCounter.estimate_tokens(text, model=model)


def calculate_cost(input_tokens: int, output_tokens: int, model: str = "gpt-3.5-turbo") -> float:
    """
    Quick cost calculator.

    Args:
        input_tokens: Input token count
        output_tokens: Output token count
        model: Model name

    Returns:
        Total cost in USD
    """
    cost, _ = CostCalculator.calculate_cost(input_tokens, output_tokens, model=model)
    return cost


def process(data: str, model: str = "default", **kwargs) -> str:
    """
    Process function for compatibility.

    Args:
        data: Input text
        model: Model name
        **kwargs: Additional options

    Returns:
        Token count as string
    """
    tokens = count_tokens(data, model=model)
    return f"Estimated tokens: {tokens}"


def main():
    """Main entry point for CLI."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Count tokens for AI models and calculate API costs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  token-counter "Your text here"                     # Count tokens
  token-counter "Your text" --model gpt-4            # Count for specific model
  token-counter "Your text" --cost 500 --model gpt-4-turbo  # Estimate cost
  token-counter "Your text" -i 1000 -o 500 --model claude-3-opus  # Full cost
        """,
    )

    parser.add_argument("text", help="Text to analyze")
    parser.add_argument("-m", "--model", default="default", help="Model name")
    parser.add_argument(
        "-c",
        "--cost",
        type=int,
        help="Estimate output tokens for cost calculation",
    )
    parser.add_argument(
        "-i",
        "--input-tokens",
        type=int,
        help="Input tokens (overrides text analysis)",
    )
    parser.add_argument(
        "-o",
        "--output-tokens",
        type=int,
        help="Output tokens for cost calculation",
    )

    args = parser.parse_args()

    if args.input_tokens is None:
        input_tokens = TokenCounter.estimate_tokens(args.text, model=args.model)
    else:
        input_tokens = args.input_tokens
    output_tokens = args.output_tokens or args.cost or 500

    print(f"Input tokens (estimated): {input_tokens}")
    known = ", ".join(sorted(CostCalculator.PRICING))
    if args.model == "default":
        print(f"Pass --model to see a cost. Priced models: {known}")
        return
    if args.model not in CostCalculator.PRICING:
        parser.error(f"no price for model '{args.model}'. Priced models: {known}")
    print(f"Output tokens: {output_tokens}")
    print()
    _, details = CostCalculator.calculate_cost(input_tokens, output_tokens, model=args.model)
    print("Cost breakdown:")
    print(json.dumps(details, indent=2))


if __name__ == "__main__":
    main()
