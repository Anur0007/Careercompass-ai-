"""Optional Google ADK agent definitions for CareerCompass AI.

This file verifies that the project can expose its architecture through the
actual Google ADK package when available. The deterministic production demo still
uses careercompass.py so the Kaggle submission remains stable without API keys.
"""

try:
    from google.adk.agents import Agent
except Exception as exc:  # pragma: no cover - environment dependent
    Agent = None
    ADK_IMPORT_ERROR = exc
else:
    ADK_IMPORT_ERROR = None


def build_adk_agent_tree():
    """Build an ADK coordinator with specialist sub-agents.

    These ADK agents document the orchestration boundaries used by the deterministic
    engine. They do not call a remote model by default, avoiding secret/API-key
    requirements for Kaggle judging.
    """
    if Agent is None:
        raise RuntimeError(f"Google ADK is not available: {ADK_IMPORT_ERROR}")

    privacy_agent = Agent(
        name="privacy_safety_agent",
        description="Masks sensitive data and validates career-planning input.",
        instruction="Mask PII, validate required fields, and add responsible career guidance notes.",
    )
    comparator_agent = Agent(
        name="career_path_comparator_agent",
        description="Compares career paths using deterministic scoring dimensions.",
        instruction="Compare configured career paths using skill, interest, feasibility, project, and time-readiness criteria.",
    )
    skill_gap_agent = Agent(
        name="skill_gap_readiness_agent",
        description="Identifies target-role skill gaps and readiness actions.",
        instruction="Create a concise skill gap matrix, resume checklist, and interview readiness topics.",
    )
    roadmap_agent = Agent(
        name="roadmap_planner_agent",
        description="Creates a deadline-aware internship preparation roadmap.",
        instruction="Use weeks until goal and weekly hours to create a practical sprint plan.",
    )
    human_approval_agent = Agent(
        name="human_approval_agent",
        description="Adds a human-in-the-loop checkpoint before final report generation.",
        instruction="Ask the user to confirm the primary path and time commitment before finalizing.",
    )
    coordinator = Agent(
        name="careercompass_coordinator",
        description="Coordinates specialist career-planning agents for CareerCompass AI.",
        instruction="Delegate to specialist agents and compose a final structured CareerCompass report.",
        sub_agents=[privacy_agent, comparator_agent, skill_gap_agent, roadmap_agent, human_approval_agent],
    )
    return coordinator


if __name__ == "__main__":
    root = build_adk_agent_tree()
    print("ADK agent tree created:", root.name)
    print("Sub-agents:", ", ".join(agent.name for agent in root.sub_agents))
