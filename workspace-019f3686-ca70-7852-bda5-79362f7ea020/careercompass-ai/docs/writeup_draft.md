# CareerCompass AI: A Multi-Agent Career Path Comparator and Internship Roadmap Planner

## Subtitle
Helping students turn career uncertainty into an explainable internship preparation roadmap.

## Track
Concierge Agents

## Problem
Students and early-career professionals often struggle to choose a realistic career path, understand skill gaps, prepare for internships, and convert vague goals into an actionable plan. Existing tools are fragmented: job boards list opportunities, course platforms list learning content, resume tools improve documents, and generic chatbots provide broad advice. But students still need a structured workflow that compares options, explains tradeoffs, and turns recommendations into a time-aware roadmap.

CareerCompass AI addresses this by acting like a small team of specialized career-planning agents. Instead of returning only paragraph advice, it produces a structured report with a career comparison matrix, explainable scoring, skill gaps, a deadline-aware internship sprint plan, and a human-in-the-loop approval step.

## What Makes This Different
The core differentiator is:

**Career Path Comparison Matrix + Deadline-Aware Internship Sprint Plan**

A generic chatbot may suggest one career path. CareerCompass AI compares multiple paths side by side using a deterministic Suitability Index, explains why the top recommendation was selected, and generates a roadmap based on the user's available time and internship deadline.

## Solution Overview
The user provides a structured student profile including education, skills, interests, projects, career goal, weekly time commitment, internship deadline, and location preference. CareerCompass AI then runs a multi-agent workflow:

1. Privacy & Safety Agent masks sensitive information and validates the profile.
2. Coordinator Agent orchestrates the pipeline.
3. Career Path Comparator Agent compares configured career paths.
4. Skill Gap & Readiness Agent identifies missing skills and preparation needs.
5. Roadmap Planner Agent generates a deadline-aware internship sprint plan.
6. Human Approval Agent allows the user to review or adjust the preferred path, weekly hours, or deadline before final report generation.

The final output is a Markdown career report with recommendations, explainable scores, skill gaps, resume/interview readiness, and a weekly preparation roadmap.

## Multi-Agent Architecture

```text
Student Profile
      ↓
Privacy & Safety Agent
      ↓
Coordinator Agent
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

| Course Concept | How CareerCompass AI Demonstrates It |
|---|---|
| ADK / Multi-Agent System | The project uses a coordinator and specialist agents for privacy, comparison, skill gaps, roadmaps, and human approval. An optional Google ADK agent tree is included in `adk_app.py` and was verified in Kaggle. |
| Agent Skills | A reusable skill file is included at `.agents/skills/career-roadmap/SKILL.md`, documenting the career-roadmap procedure and output format. |
| Security Features | The Privacy & Safety Agent masks emails, phone numbers, and secret-like values; the project stores no personal data by default and requires no API keys. |
| Human-in-the-Loop | The Human Approval Agent can change the preferred career path, weekly time commitment, and internship deadline before the roadmap is regenerated. |
| Deployability | The project runs in a Kaggle Notebook and locally from GitHub with simple Python commands. |

## Deterministic Scoring
CareerCompass AI uses an explainable Suitability Index instead of arbitrary model output:

- 35% Skill Match
- 25% Interest Match
- 20% Internship Feasibility
- 10% Project Alignment
- 10% Time-to-Readiness

Career paths and weights are configurable in `config/scoring_config.json`. The implementation validates that weights sum to 1.0. A lightweight synonym layer maps common terms such as “ML” to “machine learning,” “AI” to “artificial intelligence,” and “DSA” to “data structures and algorithms.”

## Demo Result
For a 3rd-year B.Tech CSE student seeking an AI/ML internship, CareerCompass AI recommended:

- Primary path: Machine Learning Intern
- Backup path: Data Analyst Intern
- Suitability Index: 78/100
- Key evidence: Python, machine learning, data preprocessing, Git, model evaluation
- Improvement areas: portfolio documentation, model deployment, mock interview practice
- Roadmap: 10-week internship sprint after human approval changed the deadline and weekly time commitment

The report also demonstrated privacy masking by redacting an email and phone number from the resume text.

## Evaluation
The project includes three predefined evaluation profiles:

| Test Profile | Expected Outcome | Observed Outcome |
|---|---|---|
| AI/ML Internship Seeker | Data Analyst or Machine Learning roadmap | Machine Learning Intern — PASS |
| Data Analyst Switcher | Data Analyst or Business Analyst roadmap | Data Analyst Intern — PASS |
| Backend Intern | Backend Developer or Python Developer roadmap | Backend Developer Intern — PASS |

A Kaggle reality check script also verifies privacy masking, human approval changes, scoring wording, evaluation outputs, and optional ADK agent tree creation.

## Security and Privacy
CareerCompass AI is designed to be safe for a student-facing planning workflow:

- No API keys are required for the deterministic engine.
- No personal data is persisted by default.
- Email addresses and phone numbers are masked.
- The report clearly states that recommendations are planning support, not guaranteed hiring outcomes.
- Users are encouraged to review recommendations with mentors, faculty, or career counselors.

## Limitations
This MVP expects structured profile input rather than fully free-form conversation. It does not scrape live internship listings, guarantee job outcomes, or cover every possible career field. Recommendations are limited to configured career paths and should be reviewed by a human.

## Future Work
Planned post-submission improvements include a Profile Completeness Agent for guided conversation, resume PDF parsing, RAG over job descriptions and course resources, real internship APIs, Streamlit or Gradio UI, MCP integration, and long-term progress tracking.

## Links
- GitHub Repository: https://github.com/Anur0007/Careercompass-ai-/tree/main/workspace-019f360d-6e0c-7a99-a520-4be1c32faaae/careercompass-ai
- YouTube Demo: ADD_YOUTUBE_LINK_HERE
