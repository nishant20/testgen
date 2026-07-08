"""Render a TestSuite as readable Markdown — the default, great for a PR or wiki."""

from __future__ import annotations

from ..models import TestSuite


def _escape_cell(text: str) -> str:
    """Make text safe to place inside a Markdown table cell."""
    return text.replace("|", "\\|").replace("\n", " ")


def to_markdown(suite: TestSuite) -> str:
    lines: list[str] = [
        f"# Test Suite: {suite.feature}",
        "",
        suite.summary,
        "",
        f"**{len(suite.test_cases)} test case(s)**",
        "",
    ]

    for tc in suite.test_cases:
        lines += [f"## {tc.id} — {tc.title}", ""]
        lines.append(f"- **Type:** {tc.type.value}")
        lines.append(f"- **Priority:** {tc.priority.value}")
        if tc.tags:
            lines.append(f"- **Tags:** {', '.join(tc.tags)}")
        lines.append("")

        if tc.preconditions:
            lines.append("**Preconditions:**")
            lines += [f"- {p}" for p in tc.preconditions]
            lines.append("")

        if tc.test_data:
            lines.append("**Test data:**")
            lines += [f"- {d}" for d in tc.test_data]
            lines.append("")

        lines += [
            "**Steps:**",
            "",
            "| # | Action | Expected result |",
            "| --- | --- | --- |",
        ]
        for i, step in enumerate(tc.steps, start=1):
            lines.append(
                f"| {i} | {_escape_cell(step.action)} "
                f"| {_escape_cell(step.expected_result)} |"
            )
        lines.append("")

    return "\n".join(lines)
