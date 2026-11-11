# DevTeam AI
### Your AI-Powered Multi-Agent Software Development Team

DevTeam AI is an AI-powered software development system that brings together five specialized AI agents to automate the software development workflow. Built with **CrewAI, Groq, and FastAPI**, it transforms a simple software requirement into a structured, tested, and documented Python project.

Instead of relying on a single AI assistant, DevTeam AI uses a sequential team of specialized agents, where each agent handles a specific stage of development and contributes to the final result.

---

## Project Overview

DevTeam AI accepts a natural-language software requirement and coordinates five AI agents to analyze, develop, test, review, and document the requested solution.

The system generates Python source code, automated tests, implementation plans, code reviews, technical reports, and a downloadable ZIP archive.

## AI Agent Team

| Agent | Responsibility |
|---|---|
| Requirements Analyst | Analyzes requirements and creates an implementation plan. |
| Python Developer | Generates Python source code based on the plan. |
| QA Automation Engineer | Creates pytest test cases and validates the solution. |
| Code Reviewer | Reviews the generated code and identifies potential issues. |
| Technical Report Writer | Produces the final technical documentation. |

## How It Works

```text
       USER REQUIREMENT
              |
              v
    REQUIREMENTS ANALYST
              |
              v
      PYTHON DEVELOPER
              |
              v
   QA AUTOMATION ENGINEER
              |
              v
       CODE REVIEWER
              |
              v
    TECHNICAL REPORT WRITER
              |
              v
      PROJECT GENERATION
              |
              v
       DOWNLOAD ZIP
```

Each agent performs its assigned task in sequence, using the outputs of previous stages as context.

---

## Key Features

- **Multi-Agent Architecture:** Five specialized AI agents collaborate through a sequential CrewAI workflow.
- **Automated Requirement Analysis:** Converts natural-language requirements into an implementation plan.
- **AI Code Generation:** Generates Python source code based on the analyzed requirements.
- **Automated Testing:** Creates and executes pytest test cases.
- **AI Code Review:** Evaluates generated code and highlights potential improvements.
- **Technical Documentation:** Generates implementation reports and project README files.
- **ZIP Export:** Packages generated project files into a downloadable archive.
- **FastAPI Backend:** Provides API endpoints for application health, project generation, and downloads.
- **Interactive Web Interface:** Allows users to submit requirements and access generated outputs.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| CrewAI | Multi-agent orchestration |
| Groq | Large Language Model inference |
| FastAPI | Backend API framework |
| Uvicorn | ASGI application server |
| Pytest | Automated testing |
| HTML5 | Frontend structure |
| CSS3 | Responsive interface and styling |
| JavaScript | Frontend interactions |
| ZIP | Generated project packaging |

---

## Project Structure

```text
DevTeam-AI/
│
├── agents/
│   ├── __init__.py
│   └── team.py
│
├── workflows/
│   ├── __init__.py
│   └── development_crew.py
│
├── services/
│   ├── __init__.py
│   └── artifacts.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── generated_projects/
│   └── .gitkeep
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure you have:

- Python 3.10–3.12 (recommended)
- Git
- An active Groq API key
- Internet connection

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/DevTeam-AI.git
cd DevTeam-AI
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create your environment file.

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
notepad .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

Add your Groq credentials:

```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Get your API key from the [Groq Console](https://console.groq.com/).

**Security:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the Application

```bash
python -m uvicorn app:app --reload
```

Open the application in your browser:

**http://127.0.0.1:8000**

---

## Generated Project Outputs

Every successful development workflow generates a project folder inside `generated_projects/`.

| File | Description |
|---|---|
| `solution.py` | AI-generated Python implementation |
| `test_solution.py` | Automated pytest test cases |
| `implementation_plan.md` | Requirements and implementation plan |
| `code_review.md` | AI-generated code review |
| `development_report.md` | Final technical report |
| `test_results.json` | Automated test execution results |
| `README.md` | Generated project documentation |
| `devteam_ai_output.zip` | Downloadable project archive |

---

## API Documentation

DevTeam AI exposes the following REST API endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the web interface |
| GET | `/api/health` | Checks application and API-key status |
| POST | `/api/build` | Executes the multi-agent development workflow |
| GET | `/api/download/{project_id}` | Downloads a generated project ZIP archive |

FastAPI interactive API documentation may be available at:

**http://127.0.0.1:8000/docs**

### Example API Request

```http
POST /api/build
Content-Type: application/json
```

```json
{
  "requirement": "Build a Python calculator with addition, subtraction, multiplication, division, and unit tests."
}
```

The API returns the generated development outputs and associated project information according to the application response schema.

---

## Troubleshooting

**1. Missing API Key**

- Confirm that `.env` exists in the same directory as `app.py`.
- Verify that `GROQ_API_KEY` is correctly configured.
- Restart the application after changing environment variables.

**2. Model Unavailable**

- Check the available models in the Groq model catalog.
- Update `GROQ_MODEL` in `.env` to a supported model.

**3. CrewAI / LiteLLM Errors**

Reinstall the required CrewAI integration:

```bash
python -m pip install --upgrade "crewai[litellm]"
```

**4. Python Environment Issues**

Activate the project's virtual environment before installing dependencies or running the server.

Use:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

**5. API Rate Limits**

If the model API returns a rate-limit error, reduce the size of the agent prompts and outputs, or retry when the applicable API limit allows.

---

## Security Considerations

DevTeam AI is an educational and local development prototype.

It executes AI-generated test code in a subprocess with a timeout. However, a subprocess timeout alone does not provide security isolation.

**Do not expose the application publicly or execute arbitrary untrusted generated code on a production server.**

For production deployment, use a dedicated isolated execution environment with strict CPU, memory, filesystem, process, and network restrictions. Add authentication, request limits, and appropriate API-key protection.

---

## Future Improvements

- Isolated code execution using secure containers.
- Support for multiple programming languages.
- Persistent project history and management.
- Improved automated debugging and code optimization.
- More advanced agent collaboration.
- Deployment-ready project generation.
- User authentication and project dashboards.

---

## Project Purpose

This project demonstrates how multi-agent AI systems can coordinate specialized tasks to automate a practical software engineering workflow.

It combines agent orchestration, LLM-powered code generation, automated testing, code review, and technical documentation into one application.

## Author

**Rameesha Fatima**

AI & Data Science Student

GitHub: [Rameeshafatima-png](https://github.com/Rameeshafatima-png)

---

*DevTeam AI — Turning software requirements into AI-assisted development workflows.*