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
