
from __future__ import annotations

import os
import re
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool


# Fix: CrewAI cache_breakpoint compatibility with Groq
import crewai.llms.cache as crew_cache

crew_cache.mark_cache_breakpoint = lambda msg: msg


from workflows.development_crew import run_development_workflow

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "generated_projects"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title=os.getenv("APP_NAME", "DevTeam AI"),
    description="AI-powered software development team",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class BuildRequest(BaseModel):
    requirement: str = Field(
        min_length=20,
        max_length=int(os.getenv("MAX_REQUIREMENT_CHARS", "6000"))
    )


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "model": os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        ),
    }


@app.post("/api/build")
async def build_project(payload: BuildRequest):

    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key or api_key == "your_groq_api_key_here":
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is missing. Add your Groq API key to .env and restart the server."
        )

    requirement = payload.requirement.strip()

    if len(requirement) < 20:
        raise HTTPException(
            status_code=422,
            detail="Please provide a more detailed software requirement."
        )

    project_id = uuid.uuid4().hex[:10]
    project_dir = OUTPUT_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    try:
        result = await run_in_threadpool(
            run_development_workflow,
            requirement,
            project_dir,
        )

        result["project_id"] = project_id
        result["download_url"] = (
            f"/api/download/{project_id}"
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"The agent workflow failed: "
                f"{type(exc).__name__}: {str(exc)[:500]}"
            ),
        ) from exc


@app.get("/api/download/{project_id}")
async def download_project(project_id: str):

    if not re.fullmatch(r"[a-f0-9]{10}", project_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid project ID."
        )

    project_dir = OUTPUT_DIR / project_id
    archive = project_dir / "devteam_ai_output.zip"

    if not archive.is_file():
        raise HTTPException(
            status_code=404,
            detail="Project output was not found."
        )

    return FileResponse(
        archive,
        media_type="application/zip",
        filename=f"devteam_ai_{project_id}.zip",
    )
