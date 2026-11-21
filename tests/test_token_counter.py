"""Tests for token-counter utility."""

import pytest

from token_counter import CostCalculator, TokenCounter, calculate_cost, count_tokens


class TestTokenCounter:
    """Test token counting functionality."""

    def test_count_characters(self):
        """Test character counting."""
        text = "Hello World"
        assert TokenCounter.count_characters(text) == 11

    def test_count_words(self):
        """Test word counting."""
        text = "Hello World Test"
        assert TokenCounter.count_words(text) == 3

    def test_count_lines(self):
        """Test line counting."""
        text = "Line 1\nLine 2\nLine 3"
        assert TokenCounter.count_lines(text) == 3

    def test_estimate_tokens_default(self):
        """Test token estimation with default model."""
        text = "Hello world"
        tokens = TokenCounter.estimate_tokens(text)
        assert tokens > 0
        assert isinstance(tokens, int)

    def test_estimate_tokens_different_models(self):
        """Test token estimation for different models."""
        text = "This is a test sentence to estimate tokens."

        for model in ["claude-3-opus", "gpt-4", "gpt-3.5-turbo"]:
            tokens = TokenCounter.estimate_tokens(text, model=model)
            assert tokens > 0

    def test_estimate_tokens_longer_text(self):
        """Test that longer text produces more tokens."""
        short = "Hello"
        long = "Hello " * 100

        short_tokens = TokenCounter.estimate_tokens(short)
        long_tokens = TokenCounter.estimate_tokens(long)

        assert long_tokens > short_tokens

    def test_estimate_tokens_with_overhead(self):
        """Test token estimation with overhead."""
        text = "Test text for longer estimation"
        without = TokenCounter.estimate_tokens(text, include_overhead=False)
        with_overhead = TokenCounter.estimate_tokens(text, include_overhead=True)

        assert with_overhead >= without

    def test_estimate_tokens_minimum(self):
        """Test that minimum token count is 1."""
        tokens = TokenCounter.estimate_tokens("")
        assert tokens >= 1

    def test_batch_estimate(self):
        """Test batch token estimation."""
        texts = ["Hello", "World", "Test"]
        result = TokenCounter.batch_estimate(texts)

        assert result["texts"] == 3
        assert result["total"] > 0
        assert result["average"] > 0
        assert len(result["details"]) == 3

    def test_batch_estimate_stats(self):
        """Test batch statistics."""
        texts = ["a", "test", "this is a longer text"]
        result = TokenCounter.batch_estimate(texts)

        assert result["min"] <= result["average"] <= result["max"]


class TestCostCalculator:
    """Test cost calculation functionality."""

    def test_calculate_cost_basic(self):
        """Test basic cost calculation."""
        cost, details = CostCalculator.calculate_cost(1000, 500, model="gpt-4-turbo")

        assert cost > 0
        assert details["model"] == "gpt-4-turbo"
        assert details["input_tokens"] == 1000
        assert details["output_tokens"] == 500
        assert details["total_tokens"] == 1500

    def test_calculate_cost_different_models(self):
        """Test cost calculation for different models."""
        models = ["claude-3-opus", "gpt-4", "gpt-3.5-turbo"]

        for model in models:
            cost, _ = CostCalculator.calculate_cost(1000, 500, model=model)
            assert cost > 0

    def test_calculate_cost_pricing(self):
        """Test that pricing is calculated correctly."""
        input_tokens = 1_000_000
        output_tokens = 1_000_000

        cost, details = CostCalculator.calculate_cost(
            input_tokens, output_tokens, model="gpt-4-turbo"
        )

        # gpt-4-turbo: $10/1M input, $30/1M output
        expected = 10.0 + 30.0
        assert abs(cost - expected) < 0.01

    def test_calculate_cost_invalid_model(self):
        """Test error handling for invalid model."""
        with pytest.raises(ValueError):
            CostCalculator.calculate_cost(1000, 500, model="invalid-model")

    def test_estimate_request_cost(self):
        """Test request cost estimation."""
        prompt = "Hello world"
        result = CostCalculator.estimate_request_cost(
            prompt, expected_output_tokens=100, model="gpt-4-turbo"
        )

        assert "input_tokens" in result or "input_cost" in result
        assert "total_cost" in result
        assert result["total_cost"] > 0


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_count_tokens_function(self):
        """Test count_tokens convenience function."""
        tokens = count_tokens("Hello world")
        assert tokens > 0

    def test_calculate_cost_function(self):
        """Test calculate_cost convenience function."""
        cost = calculate_cost(1000, 500)
        assert cost > 0

    def test_count_tokens_with_model(self):
        """Test count_tokens with specific model."""
        tokens = count_tokens("Test", model="gpt-4")
        assert tokens > 0


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_text(self):
        """Test with empty text."""
        tokens = TokenCounter.estimate_tokens("")
        assert tokens >= 1

    def test_very_long_text(self):
        """Test with very long text."""
        long_text = "word " * 1000
        tokens = TokenCounter.estimate_tokens(long_text)
        # 5000 chars of English is roughly 1,000-1,400 tokens
        assert 1000 <= tokens <= 1400

    def test_special_characters(self):
        """Test with special characters."""
        text = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        tokens = TokenCounter.estimate_tokens(text)
        assert tokens > 0

    def test_unicode_characters(self):
        """Test with unicode characters."""
        text = "Hello 世界 мир"
        tokens = TokenCounter.estimate_tokens(text)
        assert tokens > 0


class TestAccuracy:
    """Estimates should land near real tokenizer counts (~4 characters per token)."""

    def test_english_prose_is_about_four_chars_per_token(self):
        text = "The quick brown fox jumps over the lazy dog. " * 100  # 4,500 chars
        for model in ["gpt-4", "claude-3-opus", "default"]:
            tokens = TokenCounter.estimate_tokens(text, model=model)
            assert 900 <= tokens <= 1500, (model, tokens)


class TestCli:
    def run(self, capsys, monkeypatch, *argv):
        from token_counter.core import main

        monkeypatch.setattr("sys.argv", ["token-counter", *argv])
        main()
        return capsys.readouterr().out

    def test_default_model_explains_missing_price(self, capsys, monkeypatch):
        out = self.run(capsys, monkeypatch, "Hello world")
        assert "Input tokens (estimated):" in out
        assert "Pass --model to see a cost" in out

    def test_unknown_model_exits_with_error(self, capsys, monkeypatch):
        with pytest.raises(SystemExit) as exc:
            self.run(capsys, monkeypatch, "Hello", "-m", "not-a-model")
        assert exc.value.code == 2

    def test_explicit_token_counts_are_priced_exactly(self, capsys, monkeypatch):
        out = self.run(capsys, monkeypatch, "x", "-i", "1000", "-o", "500", "-m", "gpt-4-turbo")
        assert '"input_tokens": 1000' in out
        assert '"total_cost": 0.025' in out
