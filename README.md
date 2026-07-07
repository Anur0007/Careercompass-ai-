# CareerCompass AI

**A Multi-Agent Career Path Comparator and Internship Roadmap Planner**

CareerCompass AI helps students and early-career professionals compare career paths, understand skill gaps, and generate a deadline-aware internship preparation roadmap.

## What Makes This Different From ChatGPT?

CareerCompass AI is not a generic career chatbot. It uses a structured multi-agent workflow to:

1. Compare multiple career paths side by side.
2. Calculate a Suitability Index for each path with deterministic, explainable criteria.
3. Explain **why** the top recommendation was selected.
4. Generate a deadline-aware internship sprint plan.
5. Include a human-in-the-loop approval checkpoint before finalizing the report.


## Example Workflow

```text
Student Profile
      ↓
Privacy & Safety Agent
      ↓
Career Path Comparator
      ↓
Skill Gap Analysis
      ↓
Roadmap Planner
      ↓
Human Approval
      ↓
Career Report
```

## Course Concepts Demonstrated

| Course Concept | How This Project Demonstrates It |
|---|---|
| ADK / Multi-Agent System | Coordinator and specialist agents collaborate: Privacy & Safety, Career Path Comparator, Skill Gap & Readiness, Roadmap Planner, Human Approval. |
| Agent Skills | Reusable skill in `.agents/skills/career-roadmap/SKILL.md`. |
| Security Features | Sensitive information masking, no data retention by default, no API keys required. |
| Human-in-the-Loop | User approval checkpoint before final report generation. |
| Deployability | Runs in Kaggle Notebook and locally with simple Python commands. |

## Deterministic Career Scoring

Suitability Index =

- 35% Skill Match
- 25% Interest Match
- 20% Internship Feasibility
- 10% Project Alignment
- 10% Time-to-Readiness

Career paths and scoring weights are configurable in `config/scoring_config.json`. The implementation validates that the weights sum to `1.0` before scoring.

## Lightweight Semantic Matching

The MVP avoids embeddings or external LLM calls for reliability. Instead, it uses a small synonym dictionary so common student wording maps to canonical concepts. Examples:

| User Term | Canonical Concept |
|---|---|
| ML / basic ML | machine learning |
| AI | artificial intelligence |
| backend | backend development |
| DSA | data structures and algorithms |
| dashboarding | dashboard |

## Human-in-the-Loop Approval

Before final roadmap generation, the user can approve or modify:

- preferred career path
- weekly time commitment
- internship deadline

The roadmap is regenerated after these changes, making the approval step meaningful rather than a static checkbox.

## Run Locally

```bash
cd careercompass-ai
python careercompass.py
python evaluate_profiles.py
python clean_run_check.py
```

# CareerCompass AI Architecture

```text
Student Profile
   ↓
Privacy & Safety Agent
   ↓
Coordinator Agent
   ↓
Career Path Comparator Agent
   ↓
Skill Gap & Readiness Agent
   ↓
Roadmap Planner Agent
   ↓
Human Approval Agent
   ↓
Final CareerCompass Report
```

## Agent Responsibilities

| Agent | Purpose | Output |
|---|---|---|
| Privacy & Safety Agent | Mask sensitive data and validate profile fields | Sanitized profile and privacy notes |
| Coordinator Agent | Orchestrate the workflow and compose the report | Final Markdown report |
| Career Path Comparator Agent | Score and compare configured career paths | Career comparison matrix |
| Skill Gap & Readiness Agent | Identify missing skills and preparation needs | Skill gap matrix, resume/interview checklist |
| Roadmap Planner Agent | Build a deadline-aware sprint plan | Weekly roadmap |
| Human Approval Agent | Require review before finalizing | Approval status and adjustments |

## Course Concept Mapping

| Course Concept | Demonstration |
|---|---|
| ADK / Multi-Agent System | Coordinator and specialist agents with clear responsibilities. `adk_app.py` builds an optional actual Google ADK agent tree; `careercompass.py` provides the reliable deterministic engine. |
| Agent Skills | `.agents/skills/career-roadmap/SKILL.md` with YAML frontmatter and procedural instructions. |
| Security Features | PII masking, no data retention by default, no API keys required. |
| Human-in-the-Loop | Human Approval Agent before final report generation. |
| Deployability | Runs in Kaggle Notebook and locally from GitHub. |

## Repository Structure

```text
careercompass-ai/
├── README.md
├── requirements.txt
├── careercompass.py
├── evaluate_profiles.py
├── config/scoring_config.json
├── examples/
├── docs/
├── assets/architecture_diagram.svg
├── assets/screenshot_notebook_output.svg
├── assets/screenshot_comparison_table.svg
├── assets/screenshot_score_explanation.svg
├── assets/screenshot_roadmap.svg
├── docs/sample_report.md
└── .agents/skills/career-roadmap/SKILL.md
```

## Evaluation Profiles

| Test Profile | Expected Outcome |
|---|---|
| AI/ML Internship Seeker | Data Analyst or ML internship roadmap |
| Data Analyst Switcher | Data Analyst or Business Analyst roadmap |
| Backend Intern | Backend Developer or Python Developer roadmap |

Run `python evaluate_profiles.py` to generate observed outcomes.

## Security and Privacy

- Emails, phone numbers, and API-key-like values are masked.
- No user data is stored by default.
- The MVP does not require external APIs or secrets.
- Recommendations are planning support, not guaranteed hiring outcomes.

## Limitations

- Does not scrape live internships.
- Does not guarantee job placement.
- Uses configurable role definitions rather than live labor-market data.

## Future Improvements

- Resume PDF parsing
- Real internship/job APIs
- RAG over career resources
- Streamlit or Gradio UI
- MCP server integration
- Cloud deployment
