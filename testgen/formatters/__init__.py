"""Output formatters: read a TestSuite and render it for humans or tools.

Adding a new output (Gherkin, a Jira/qTest-style CSV, an HTML report) is just a
new function registered here — nothing else in the pipeline changes.
"""

from ..models import TestSuite
from .csv_fmt import to_csv
from .json_fmt import to_json
from .markdown import to_markdown

_FORMATTERS = {
    "markdown": to_markdown,
    "csv": to_csv,
    "json": to_json,
}


def render(suite: TestSuite, fmt: str) -> str:
    """Render a suite in the named format."""
    try:
        formatter = _FORMATTERS[fmt]
    except KeyError:
        raise ValueError(
            f"Unknown format '{fmt}'. Choose from: {', '.join(_FORMATTERS)}"
        )
    return formatter(suite)


def available_formats() -> list[str]:
    return list(_FORMATTERS)


__all__ = ["render", "available_formats", "to_markdown", "to_csv", "to_json"]
