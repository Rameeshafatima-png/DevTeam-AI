
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from crewai import Crew, LLM, Process, Task
from dotenv import load_dotenv

from agents.team import create_agents
from services.artifacts import (
    clean_code_block,
    create_readme,
    write_json,
    write_text,
    make_archive,
)

load_dotenv()


def _llm() -> LLM:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model_id = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    ).strip()

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    model = (
        model_id
        if model_id.startswith("groq/")
        else f"groq/{model_id}"
    )

    return LLM(
        model=model,
        api_key=api_key,
        temperature=0.2,
        max_tokens=3500,
    )


def _run_tests(project_dir: Path) -> dict:
    """Run generated pytest tests with a timeout."""

    timeout = int(os.getenv("TEST_TIMEOUT_SECONDS", "12"))

    test_file = project_dir / "test_solution.py"
    solution_file = project_dir / "solution.py"

    if not test_file.exists():
        return {
            "status": "not_run",
            "passed": 0,
            "failed": 0,
            "output": "No test file was generated.",
        }

    if not solution_file.exists():
        return {
            "status": "not_run",
            "passed": 0,
            "failed": 0,
            "output": "No solution.py was generated.",
        }

    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "test_solution.py",
            ],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
            },
        )

        output = (
            completed.stdout + "\n" + completed.stderr
        ).strip()[-6000:]

        passed_match = re.search(
            r"(\d+)\s+passed",
            output,
            flags=re.IGNORECASE,
        )

        failed_match = re.search(
            r"(\d+)\s+(?:failed|error)s?",
            output,
            flags=re.IGNORECASE,
        )

        passed = (
            int(passed_match.group(1))
            if passed_match else 0
        )

        failed = (
            int(failed_match.group(1))
            if failed_match else 0
        )

        if completed.returncode == 0:
            status = "passed"
        elif completed.returncode == 5:
            status = "not_run"
        else:
            status = "failed"

        return {
            "status": status,
            "return_code": completed.returncode,
            "passed": passed,
            "failed": failed,
            "output": output or "No pytest output.",
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "passed": 0,
            "failed": 0,
            "output": f"Tests exceeded {timeout} seconds.",
        }

    except Exception as exc:
        return {
            "status": "error",
            "passed": 0,
            "failed": 0,
            "output": f"{type(exc).__name__}: {exc}",
        }


def run_development_workflow(
    requirement: str,
    project_dir: Path,
) -> dict:

    project_dir.mkdir(parents=True, exist_ok=True)

    agents = create_agents(_llm())

    # AGENT 1: Requirements Analyst
    plan_task = Task(
        description=(
            "Analyze this software requirement:\n"
            "{requirement}\n\n"
            "Return a SHORT implementation plan containing:\n"
            "1. Project summary\n"
            "2. Essential features\n"
            "3. Inputs and outputs\n"
            "4. Main functions/modules\n"
            "5. Important validation and edge cases\n"
            "6. Acceptance criteria\n\n"
            "Maximum 700 words. Do not write code."
        ),
        expected_output=(
            "A concise implementation plan in Markdown."
        ),
        agent=agents["analyst"],
    )

    # AGENT 2: Python Developer
    code_task = Task(
        description=(
            "Implement the software requirement using Python.\n\n"
            "Requirement: {requirement}\n\n"
            "Follow the analyst's implementation plan.\n"
            "Return ONE complete Python source file in a single "
            "```python code block.\n"
            "Use readable, modular, runnable code.\n"
            "Include input validation and error handling.\n"
            "Prefer standard library dependencies.\n"
            "Do not include tests or lengthy explanations.\n"
            "Keep the implementation focused on the required features."
        ),
        expected_output=(
            "One complete Python source file in a Python code block."
        ),
        agent=agents["developer"],
        context=[plan_task],
    )

    # AGENT 3: QA Testing Engineer
    test_task = Task(
        description=(
            "Create pytest tests for the developer's exact "
            "implementation.\n\n"
            "Assume the implementation is saved as solution.py.\n"
            "Inspect its actual public functions and imports.\n"
            "Return ONE complete test_solution.py file in a "
            "single ```python code block.\n"
            "Cover important normal cases, invalid inputs, "
            "and edge cases.\n"
            "Do not invent function names or rewrite the application."
        ),
        expected_output=(
            "A complete, concise pytest test file."
        ),
        agent=agents["tester"],
        context=[code_task],
    )

    # AGENT 4: Code Reviewer
    review_task = Task(
        description=(
            "Review the generated Python implementation and tests.\n\n"
            "Identify only important issues involving:\n"
            "1. Correctness\n"
            "2. Input validation\n"
            "3. Error handling\n"
            "4. Security\n"
            "5. Maintainability\n"
            "6. Test coverage\n\n"
            "Give severity and practical recommendations.\n"
            "Maximum 600 words.\n"
            "Do not repeat the source code.\n"
            "Do not claim tests passed; the application executes them."
        ),
        expected_output=(
            "A concise code review with prioritized findings."
        ),
        agent=agents["reviewer"],
        context=[code_task, test_task],
    )

    # AGENT 5: Technical Report Writer
    report_task = Task(
        description=(
            "Write a concise final development report.\n\n"
            "Requirement: {requirement}\n\n"
            "Include project overview, implementation summary, "
            "generated files, important review findings, and limitations.\n"
            "Maximum 500 words.\n"
            "Do not reproduce source code or invent test results.\n"
            "The application will append actual pytest results later."
        ),
        expected_output=(
            "A professional and concise Markdown development report."
        ),
        agent=agents["report_writer"],
        context=[plan_task, review_task],
    )

    # Sequential five-agent workflow
    crew = Crew(
        agents=list(agents.values()),
        tasks=[
            plan_task,
            code_task,
            test_task,
            review_task,
            report_task,
        ],
        process=Process.sequential,
        verbose=False,
        memory=False,
    )

    crew.kickoff(
        inputs={
            "requirement": requirement[:6000]
        }
    )

    # Collect agent outputs
    plan = str(
        plan_task.output.raw if plan_task.output else ""
    )

    code_raw = str(
        code_task.output.raw if code_task.output else ""
    )

    tests_raw = str(
        test_task.output.raw if test_task.output else ""
    )

    review = str(
        review_task.output.raw if review_task.output else ""
    )

    report = str(
        report_task.output.raw if report_task.output else ""
    )

    # Extract generated Python files
    code = clean_code_block(code_raw, "python")
    tests = clean_code_block(tests_raw, "python")

    if not code.strip():
        raise RuntimeError(
            "Developer agent did not return usable Python code."
        )

    if not tests.strip():
        raise RuntimeError(
            "QA agent did not return usable pytest code."
        )

    # Save generated artifacts
    write_text(
        project_dir / "implementation_plan.md",
        plan,
    )

    write_text(
        project_dir / "solution.py",
        code,
    )

    write_text(
        project_dir / "test_solution.py",
        tests,
    )

    write_text(
        project_dir / "code_review.md",
        review,
    )

    # Execute generated tests locally.
    # This subprocess is NOT a security sandbox.
    test_result = _run_tests(project_dir)

    report_with_results = (
        report.strip()
        + "\n\n## Verified Test Execution\n\n"
        + f"- **Status:** {test_result['status']}\n"
        + f"- **Passed:** {test_result['passed']}\n"
        + f"- **Failed:** {test_result['failed']}\n\n"
        + "### Pytest Output\n\n```text\n"
        + test_result["output"]
        + "\n```\n"
    )

    write_text(
        project_dir / "development_report.md",
        report_with_results,
    )

    create_readme(project_dir, requirement)

    write_json(
        project_dir / "test_results.json",
        test_result,
    )

    write_json(
        project_dir / "project_metadata.json",
        {
            "requirement": requirement,
            "test_status": test_result["status"],
        },
    )

    make_archive(project_dir)

    return {
        "requirement": requirement,
        "plan": plan,
        "code": code,
        "tests": tests,
        "review": review,
        "report": report_with_results,
        "test_results": test_result,
        "files": [
            "solution.py",
            "test_solution.py",
            "implementation_plan.md",
            "code_review.md",
            "development_report.md",
            "test_results.json",
            "README.md",
        ],
    }
