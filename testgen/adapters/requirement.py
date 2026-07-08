"""Adapter for plain-English requirements and user stories — the first input
`testgen` supports. Later adapters (API specs, source code) live alongside this
one and produce the same `GenerationContext`.
"""

from __future__ import annotations

from .base import GenerationContext, InputAdapter


class RequirementAdapter(InputAdapter):
    """Turns a requirement / user story (and optional extra guidance) into a context."""

    source_type = "requirement"

    def __init__(self, text: str, instructions: str = "") -> None:
        self.text = text
        self.instructions = instructions

    def build_context(self) -> GenerationContext:
        return GenerationContext(
            source_type=self.source_type,
            content=self.text,
            instructions=self.instructions,
        )
