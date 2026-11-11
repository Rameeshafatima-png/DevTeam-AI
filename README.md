# DevTeam AI

A FastAPI application powered by a sequential CrewAI team of five agents:
1. Requirements Analyst
2. Python Developer
3. QA Automation Engineer
4. Code Reviewer
5. Technical Report Writer

The app accepts a software requirement, creates a plan, generates Python source and pytest tests, runs the tests, performs a code review, and packages the outputs into a ZIP archive.

## Requirements

- Python 3.10–3.12 recommended
- A Groq API key
- Internet access for the model API

## Windows PowerShell setup

```powershell
cd path\to\DevTeam-AI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Add your key to `.env`:

```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Run the application:

```powershell
python -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000

## macOS / Linux setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`, then run:

```bash
python -m uvicorn app:app --reload
```

## Generated project outputs

Every successful run creates a folder under `generated_projects/` containing:
- `solution.py`
- `test_solution.py`
- `implementation_plan.md`
- `code_review.md`
- `development_report.md`
- `test_results.json`
- `README.md`
- `devteam_ai_output.zip`

## Troubleshooting

**Missing API key:** Make sure `.env` is in the same folder as `app.py`, and the variable is named `GROQ_API_KEY`.

**Model unavailable:** Check the current model IDs in the Groq model catalog and update `GROQ_MODEL` in `.env`. The default is `openai/gpt-oss-120b`.

**CrewAI / LiteLLM provider errors:** Confirm that `crewai[litellm]` installed successfully. Reinstall with `python -m pip install --upgrade "crewai[litellm]"`.

**Wrong Python environment:** Always run `python -m pip` and `python -m uvicorn` after activating the project `.venv`.

## Important security limitation

This is an educational/local development prototype. It runs AI-generated test code in a subprocess with a timeout. A subprocess timeout is not a security sandbox. Do not expose this endpoint publicly or run arbitrary untrusted generated code on a production server. For production, use isolated containers or a dedicated sandbox service with strict CPU, memory, filesystem, process, and network restrictions.

## API

- `GET /api/health` — application and API-key status
- `POST /api/build` — run the five-agent workflow
- `GET /api/download/{project_id}` — download the generated ZIP
