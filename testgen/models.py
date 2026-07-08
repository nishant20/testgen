"""The shared data contract for the whole tool.

Every input adapter produces test cases in this shape, and every output
formatter consumes it. Keeping the model here — independent of both the Claude
call and the CLI — is what lets us add new inputs (API specs, source code) and
new outputs (Gherkin, Jira CSV) later without touching the core.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """How important it is that this case passes before release."""

    critical = "Critical"
    high = "High"
    medium = "Medium"
    low = "Low"


class TestType(str, Enum):
    """The category of coverage a test case provides."""

    functional = "Functional"
    negative = "Negative"
    boundary = "Boundary"
    security = "Security"
    usability = "Usability"
    performance = "Performance"


class TestStep(BaseModel):
    """A single action a tester performs and what they should observe."""

    action: str = Field(description="The concrete action the tester performs.")
    expected_result: str = Field(
        description="The observable result that must occur for this step to pass."
    )


class TestCase(BaseModel):
    """One self-contained, executable test case."""

    id: str = Field(description="Stable identifier, e.g. TC-001.")
    title: str = Field(description="Short summary of what this case verifies.")
    type: TestType
    priority: Priority
    preconditions: list[str] = Field(
        description="State that must be true before the steps run."
    )
    steps: list[TestStep]
    test_data: list[str] = Field(
        description="Concrete input values or fixtures the case needs."
    )
    tags: list[str] = Field(
        description="Free-form labels for filtering, e.g. smoke, regression, auth."
    )


class TestSuite(BaseModel):
    """A generated set of test cases for one feature or requirement."""

    feature: str = Field(description="The feature or requirement under test.")
    summary: str = Field(
        description="One-paragraph overview of the testing approach and coverage."
    )
    test_cases: list[TestCase]
