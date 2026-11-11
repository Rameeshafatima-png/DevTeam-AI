
from crewai import Agent, LLM


def create_agents(llm: LLM) -> dict[str, Agent]:
    """Create five specialized, token-efficient development agents."""

    analyst = Agent(
        role="Requirements Analyst",
        goal=(
            "Analyze the user's idea and produce a concise implementation plan "
            "with features, inputs, outputs, and acceptance criteria."
        ),
        backstory=(
            "You are a practical software analyst. Focus on essential requirements, "
            "scope, assumptions, and important edge cases. Avoid unnecessary explanations."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=2,
    )

    developer = Agent(
        role="Python Developer",
        goal=(
            "Generate complete, runnable Python code that implements the approved plan."
        ),
        backstory=(
            "You are an experienced Python developer. Write clean, modular code "
            "with validation and error handling. Avoid unnecessary dependencies. "
            "Return complete source files, not lengthy explanations."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=2,
    )

    tester = Agent(
        role="QA Testing Engineer",
        goal=(
            "Create concise pytest tests that match the actual generated code."
        ),
        backstory=(
            "You are a QA engineer. Cover normal cases, invalid inputs, and important "
            "edge cases. Do not invent functions or claim tests passed without execution."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=2,
    )

    reviewer = Agent(
        role="Python Code Reviewer",
        goal=(
            "Review the generated source code and tests. Identify important bugs "
            "and provide specific improvements."
        ),
        backstory=(
            "You review Python code for correctness, reliability, security, "
            "maintainability, and test coverage. Prioritize real issues. "
            "Avoid repeating the implementation."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=2,
    )

    report_writer = Agent(
        role="Technical Report Writer",
        goal=(
            "Create a concise final report describing the project and its actual results."
        ),
        backstory=(
            "You are a technical documentation specialist. Summarize the requirements, "
            "implementation, generated files, test results, review findings, and limitations. "
            "Never claim unverified work is complete."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=2,
    )

    return {
        "analyst": analyst,
        "developer": developer,
        "tester": tester,
        "reviewer": reviewer,
        "report_writer": report_writer,
    }
