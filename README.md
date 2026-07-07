# CareerCompass AI Report

## 1. Profile Summary
- Education: B.Tech Computer Science, 3rd year
- Career goal: Get an AI/ML internship in 3 months
- Weekly time commitment: 12 hours
- Deadline: 10 weeks

## 2. Privacy & Safety Notes
- Masked 1 email value(s).
- Masked 1 phone value(s).
- No profile data is persisted by default; analysis runs in-memory.
- CareerCompass AI provides planning support, not guaranteed hiring outcomes. Please verify opportunities independently and consult mentors when possible.

## 3. Career Path Comparison Matrix
### Quick Scoreboard
| Career | Suitability Index | Confidence |
|---|---:|---|
| Machine Learning Intern | **78** | High |
| Data Analyst Intern | **47** | Medium |
| Python Developer Intern | **39** | Developing |

### Detailed Score Breakdown
| Career Path | Suitability Index | Skill Match | Interest Match | Feasibility | Project Alignment | Time Readiness | Difficulty |
|---|---:|---:|---:|---:|---:|---:|---|
| Machine Learning Intern | 78 | 100 | 67 | 68 | 29 | 100 | High |
| Data Analyst Intern | 47 | 38 | 17 | 90 | 14 | 100 | Medium |
| Python Developer Intern | 39 | 25 | 17 | 80 | 0 | 100 | Medium |

### Scoring Formula
Suitability Index = 35% Skill Match + 25% Interest Match + 20% Internship Feasibility + 10% Project Alignment + 10% Time-to-Readiness
- Weight normalization check: **1.0**

## 4. Recommendation
- Primary path: **Machine Learning Intern**
- Backup path: **Data Analyst Intern**

### Why Machine Learning Intern?
- ✓ Machine Learning Intern is recommended because of good current skill overlap (100/100); strong interest alignment (67/100); realistic preparation timeline; matched skills: data preprocessing, git, machine learning, model evaluation. The human approval step selected this as the preferred final direction.
- ✓ Current evidence: data preprocessing, git, machine learning, model evaluation
- ✓ Interest alignment: ai, data science, machine learning, ml
- ✓ Timeline considered: roadmap uses the approved deadline and weekly hours.

**Needs improvement:**
- portfolio documentation
- model deployment
- mock interview practice

### Explainable Suitability Contribution
| Component | Points Contributed | Max Points |
|---|---:|---:|
| Skill Match | 35.0 | 35 |
| Interest Match | 16.8 | 25 |
| Feasibility | 13.6 | 20 |
| Projects | 2.9 | 10 |
| Timeline | 10.0 | 10 |
| **Suitability Index** | **78** | **100** |

## 5. Skill Gap Matrix
| Skill | Current Status | Priority |
|---|---|---|
| portfolio documentation | Gap or weak evidence | High |
| model deployment | Gap or weak evidence | High |
| mock interview practice | Gap or weak evidence | High |

## 6. Resume & Interview Readiness
### Resume checklist
- Rewrite project bullets using action + tool + measurable outcome.
- Add GitHub links for the strongest 1–2 projects.
- Move target-role skills near the top of the resume.
- Add evidence for priority skills: portfolio documentation, model deployment, mock interview practice.

### Interview topics
- portfolio documentation
- model deployment
- mock interview practice
- project explanation
- behavioral questions

## 7. Deadline-Aware Internship Sprint Plan
Duration: **10 weeks** at **12 hours/week**
- Week 1: **Foundation building** — Study/practice portfolio documentation; Document learning notes
- Week 2: **Foundation building** — Study/practice model deployment; Document learning notes
- Week 3: **Foundation building** — Study/practice mock interview practice; Document learning notes
- Week 4: **Portfolio project** — Build or improve one target-role project; Commit progress to GitHub; Write README with problem, approach, and result
- Week 5: **Portfolio project** — Build or improve one target-role project; Commit progress to GitHub; Write README with problem, approach, and result
- Week 6: **Resume and interview preparation** — Update resume bullets; Practice interview questions; Prepare 90-second project explanation
- Week 7: **Resume and interview preparation** — Update resume bullets; Practice interview questions; Prepare 90-second project explanation
- Week 8: **Resume and interview preparation** — Update resume bullets; Practice interview questions; Prepare 90-second project explanation
- Week 9: **Applications and iteration** — Apply to 5–10 relevant internships; Track applications; Revise resume based on feedback
- Week 10: **Applications and iteration** — Apply to 5–10 relevant internships; Track applications; Revise resume based on feedback

## 8. Human-in-the-Loop Approval
- Approved: True
- User adjustment: User approved ML as target path and increased weekly commitment.
- Applied changes before final roadmap generation:
  - preferred_career_path: Machine Learning Intern
  - weekly_time_commitment: 12
  - weeks_until_goal: 10
- Confirm the primary career path matches your real preference.
- Confirm the weekly time commitment is realistic.
- Review roadmap with a mentor, faculty member, or career counselor if possible.

## 9. Limitations
- This prototype does not scrape live internships or guarantee job outcomes.
- Recommendations are based on configurable role definitions and should be reviewed by a human.
- Future versions can add resume parsing, job APIs, RAG, and a deployed UI.

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
