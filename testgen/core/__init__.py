"""The generation engine: build a prompt from a context, call Claude, and parse
the reply into a validated TestSuite."""

from .generator import DEFAULT_MODEL, TestCaseGenerator

__all__ = ["DEFAULT_MODEL", "TestCaseGenerator"]
