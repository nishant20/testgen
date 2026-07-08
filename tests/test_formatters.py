"""Formatter tests — these run offline (no API calls) by building a TestSuite by
hand and checking each renderer. Good first tests to have green in CI."""

import json

import pytest

from testgen.formatters import render
from testgen.models import Priority, TestCase, TestStep, TestSuite, TestType


def sample_suite() -> TestSuite:
    return TestSuite(
        feature="Password reset",
        summary="Covers the happy path and key negative cases for password reset.",
        test_cases=[
            TestCase(
                id="TC-001",
                title="Successful password reset via email link",
                type=TestType.functional,
                priority=Priority.high,
                preconditions=["User account exists", "User is logged out"],
                steps=[
                    TestStep(
                        action="Click 'Forgot password' on the login page",
                        expected_result="The reset request form is displayed",
                    ),
                    TestStep(
                        action="Enter a registered email and submit",
                        expected_result="A confirmation message is shown",
                    ),
                ],
                test_data=["email: user@example.com"],
                tags=["smoke", "auth"],
            )
        ],
    )


def test_json_roundtrips():
    data = json.loads(render(sample_suite(), "json"))
    assert data["feature"] == "Password reset"
    assert data["test_cases"][0]["id"] == "TC-001"
    assert len(data["test_cases"][0]["steps"]) == 2


def test_markdown_has_key_fields():
    out = render(sample_suite(), "markdown")
    assert "# Test Suite: Password reset" in out
    assert "## TC-001" in out
    assert "Expected result" in out


def test_csv_has_header_and_row():
    out = render(sample_suite(), "csv")
    assert out.splitlines()[0].startswith("ID,Title,Type,Priority")
    assert "TC-001" in out


def test_unknown_format_raises():
    with pytest.raises(ValueError):
        render(sample_suite(), "xml")
