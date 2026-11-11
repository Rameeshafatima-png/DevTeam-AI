from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


def clean_code_block(value: str, language: str = "python") -> str:
    """Extract the first fenced code block, or return the response if none exists."""
    text = (value or "").strip()
    pattern = rf"```(?:{re.escape(language)}|py)?\s*\n(.*?)```"
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip() + "\n"
    # Remove accidental leading/trailing markdown fences.
    text = re.sub(r"^```\w*\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.write_text(content or "", encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def create_readme(project_dir: Path, requirement: str) -> None:
    readme = f"""# Generated Python Project

## Original requirement

{requirement}

## Files

- `solution.py` — generated implementation
- `test_solution.py` — generated pytest tests
- `implementation_plan.md` — requirement analysis and plan
- `code_review.md` — reviewer findings
- `development_report.md` — final development report and actual test output
- `test_results.json` — machine-readable test result

## Run locally

```bash
python solution.py
```

## Run tests

```bash
python -m pip install pytest
python -m pytest -q
```

## Important safety note

AI-generated code can contain defects. Review it before use. The demo executes generated tests in a subprocess with a timeout, but this is **not** a hardened sandbox. Do not use this project as a public service for running arbitrary untrusted code without OS/container isolation.
"""
    write_text(project_dir / "README.md", readme)


def make_archive(project_dir: Path) -> Path:
    archive = project_dir / "devteam_ai_output.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in project_dir.iterdir():
            if path.is_file() and path.name != archive.name:
                zf.write(path, arcname=path.name)
    return archive
