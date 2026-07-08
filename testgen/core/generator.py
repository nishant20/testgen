"""The heart of the tool: hand a GenerationContext to Claude and get back a
validated TestSuite.

We use the Anthropic SDK's `messages.parse()` with our Pydantic `TestSuite` as
the output schema. That constrains the model to return exactly the shape our
formatters expect — no brittle text parsing, and validation happens for free.
"""

from __future__ import annotations

import anthropic

from ..adapters.base import GenerationContext
from ..models import TestSuite
from .prompts import SYSTEM_PROMPT

DEFAULT_MODEL = "claude-opus-4-8"


class TestCaseGenerator:
    """Generates a TestSuite from a context using Claude."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        client: anthropic.Anthropic | None = None,
        max_tokens: int = 16000,
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens
        # A bare client resolves credentials from the environment (ANTHROPIC_API_KEY
        # or an `ant auth login` profile) — see the README's Configuration section.
        self.client = client or anthropic.Anthropic()

    def generate(self, context: GenerationContext) -> TestSuite:
        response = self.client.messages.parse(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": context.to_prompt()}],
            output_format=TestSuite,
        )
        suite = response.parsed_output
        if suite is None:
            raise RuntimeError(
                "The model did not return a valid test suite "
                f"(stop_reason={response.stop_reason})."
            )
        return suite
