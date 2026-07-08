"""Render a TestSuite as JSON — the machine-readable form, for feeding another
tool or a future test-management exporter."""

from __future__ import annotations

from ..models import TestSuite


def to_json(suite: TestSuite) -> str:
    return suite.model_dump_json(indent=2)
