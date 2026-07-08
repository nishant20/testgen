"""The adapter contract.

An adapter's only job is to normalize some input into a `GenerationContext`.
The core generator never learns what the original source was — it only ever
sees a context. That indirection is what makes the requirement/API-spec/
source-code inputs interchangeable.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GenerationContext:
    """Everything the generator needs to produce a test suite, source-agnostic."""

    source_type: str
    """A short label for where this came from, e.g. "requirement"."""

    content: str
    """The raw material to derive test cases from."""

    instructions: str = ""
    """Optional extra guidance to fold into the prompt (e.g. "focus on security")."""

    def to_prompt(self) -> str:
        """Render this context as the user-turn message sent to Claude."""
        parts = [
            f"Source type: {self.source_type}",
            "",
            "Generate a thorough test suite for the following:",
            "",
            self.content.strip(),
        ]
        if self.instructions.strip():
            parts += ["", "Additional instructions:", self.instructions.strip()]
        return "\n".join(parts)


class InputAdapter(ABC):
    """Base class for all input adapters."""

    source_type: str

    @abstractmethod
    def build_context(self) -> GenerationContext:
        """Produce the normalized context for this input."""
        raise NotImplementedError
