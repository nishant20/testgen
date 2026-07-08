"""Command-line entry point for testgen."""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path
from typing import Optional

import typer

from .adapters.requirement import RequirementAdapter
from .core.generator import DEFAULT_MODEL, TestCaseGenerator
from .formatters import render

app = typer.Typer(
    add_completion=False,
    help="Generate structured test cases from software requirements using Claude.",
)


class OutputFormat(str, Enum):
    markdown = "markdown"
    csv = "csv"
    json = "json"


def _read_requirement(text: Optional[str], file: Optional[Path]) -> str:
    """Resolve the requirement from an argument, a file, or piped stdin."""
    if file is not None:
        if not file.exists():
            typer.echo(f"Error: file not found: {file}", err=True)
            raise typer.Exit(code=2)
        return file.read_text(encoding="utf-8")
    if text:
        return text
    if not sys.stdin.isatty():  # content piped in
        data = sys.stdin.read()
        if data.strip():
            return data
    typer.echo(
        "Error: provide a requirement as an argument, with --file, or via stdin.",
        err=True,
    )
    raise typer.Exit(code=2)


@app.command()
def generate(
    requirement: Optional[str] = typer.Argument(
        None, help="Requirement / user story text. Omit to use --file or stdin."
    ),
    file: Optional[Path] = typer.Option(
        None, "--file", "-f", help="Read the requirement from a file."
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.markdown, "--format", help="Output format."
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Write to a file instead of stdout."
    ),
    model: str = typer.Option(DEFAULT_MODEL, "--model", help="Claude model to use."),
    instructions: Optional[str] = typer.Option(
        None,
        "--instructions",
        "-i",
        help="Extra guidance, e.g. 'focus on security and boundary cases'.",
    ),
) -> None:
    """Generate test cases from a requirement or user story."""
    text = _read_requirement(requirement, file)
    adapter = RequirementAdapter(text, instructions=instructions or "")
    generator = TestCaseGenerator(model=model)

    typer.echo(f"Generating test cases with {model}...", err=True)
    try:
        suite = generator.generate(adapter.build_context())
    except Exception as exc:  # keep the CLI friendly; detail goes to stderr
        typer.echo(f"Generation failed: {exc}", err=True)
        raise typer.Exit(code=1)

    rendered = render(suite, format.value)
    if output is not None:
        output.write_text(rendered, encoding="utf-8")
        typer.echo(
            f"Wrote {len(suite.test_cases)} test case(s) to {output}", err=True
        )
    else:
        typer.echo(rendered)


if __name__ == "__main__":
    app()
