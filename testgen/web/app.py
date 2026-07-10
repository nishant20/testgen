"""FastAPI app for the local web UI.

This module is orchestration only: it wires HTTP requests to the same
`RequirementAdapter`, `TestCaseGenerator`, and `render()` the CLI (`testgen/cli.py`)
already uses. No generation or formatting logic lives here.
"""

from __future__ import annotations

import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ..adapters.requirement import RequirementAdapter
from ..core.generator import DEFAULT_MODEL, TestCaseGenerator
from ..formatters import render
from ..models import TestSuite

STATIC_DIR = Path(__file__).parent / "static"

_MEDIA_TYPES = {
    "markdown": "text/markdown",
    "csv": "text/csv",
    "json": "application/json",
}
_EXTENSIONS = {"markdown": "md", "csv": "csv", "json": "json"}

app = FastAPI(title="testgen")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class GenerateRequest(BaseModel):
    requirement: str
    instructions: str = ""
    model: str = DEFAULT_MODEL


class ExportRequest(BaseModel):
    suite: TestSuite
    format: str


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "testsuite"


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/generate")
def generate(req: GenerateRequest) -> TestSuite:
    adapter = RequirementAdapter(req.requirement, instructions=req.instructions)
    generator = TestCaseGenerator(model=req.model)
    try:
        return generator.generate(adapter.build_context())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/export")
def export(req: ExportRequest) -> Response:
    try:
        rendered = render(req.suite, req.format)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    ext = _EXTENSIONS[req.format]
    filename = f"{_slugify(req.suite.feature)}.{ext}"
    return Response(
        content=rendered,
        media_type=_MEDIA_TYPES[req.format],
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
