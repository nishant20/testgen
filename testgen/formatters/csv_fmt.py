"""Render a TestSuite as CSV — one row per test case, ready to import into most
test-management tools (Jira/Xray, TestRail, qTest, a spreadsheet)."""

from __future__ import annotations

import csv
import io

from ..models import TestSuite

_HEADER = [
    "ID",
    "Title",
    "Type",
    "Priority",
    "Preconditions",
    "Steps",
    "Expected Results",
    "Test Data",
    "Tags",
]


def to_csv(suite: TestSuite) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(_HEADER)

    for tc in suite.test_cases:
        steps = "\n".join(f"{i}. {s.action}" for i, s in enumerate(tc.steps, 1))
        expected = "\n".join(
            f"{i}. {s.expected_result}" for i, s in enumerate(tc.steps, 1)
        )
        writer.writerow(
            [
                tc.id,
                tc.title,
                tc.type.value,
                tc.priority.value,
                "\n".join(tc.preconditions),
                steps,
                expected,
                "\n".join(tc.test_data),
                ", ".join(tc.tags),
            ]
        )

    return buf.getvalue()
