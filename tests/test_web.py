"""Web API tests — these run offline (no Anthropic API calls) by posting a
hand-built suite straight to /api/export and checking it matches render()."""

import json

from fastapi.testclient import TestClient

from testgen.formatters import render
from testgen.models import Priority, TestCase, TestStep, TestSuite, TestType
from testgen.web.app import app

client = TestClient(app)


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
                ],
                test_data=["email: user@example.com"],
                tags=["smoke", "auth"],
            )
        ],
    )


def test_index_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_export_markdown_matches_formatter():
    suite = sample_suite()
    response = client.post(
        "/api/export", json={"suite": suite.model_dump(mode="json"), "format": "markdown"}
    )
    assert response.status_code == 200
    assert response.text == render(suite, "markdown")
    assert response.headers["content-disposition"].endswith('.md"')


def test_export_csv_matches_formatter():
    suite = sample_suite()
    response = client.post(
        "/api/export", json={"suite": suite.model_dump(mode="json"), "format": "csv"}
    )
    assert response.status_code == 200
    assert response.text == render(suite, "csv")
    assert response.headers["content-disposition"].endswith('.csv"')


def test_export_json_matches_formatter():
    suite = sample_suite()
    response = client.post(
        "/api/export", json={"suite": suite.model_dump(mode="json"), "format": "json"}
    )
    assert response.status_code == 200
    assert json.loads(response.text) == json.loads(render(suite, "json"))


def test_export_unknown_format_returns_400():
    suite = sample_suite()
    response = client.post(
        "/api/export", json={"suite": suite.model_dump(mode="json"), "format": "xml"}
    )
    assert response.status_code == 400
