# CareerCompass AI — 5 Minute Demo Script

Target length: 4:30–4:50

## 0:00–0:25 — Opening / Problem
Hi, this is CareerCompass AI, a multi-agent career path comparator and internship roadmap planner built for the Kaggle AI Agents capstone.

Students often struggle with choosing a career path, understanding skill gaps, preparing for internships, and converting vague goals into a concrete action plan. Generic chatbots usually give broad advice, but students need explainable, personalized, time-aware guidance.

## 0:25–0:50 — Solution / Differentiator
CareerCompass AI is different because it does not just give one paragraph of career advice. It compares multiple career paths side by side, calculates an explainable Suitability Index, identifies skill gaps, and generates a deadline-aware internship sprint plan.

The core differentiator is: Career Path Comparison Matrix plus Deadline-Aware Internship Roadmap.

## 0:50–1:30 — Architecture
Show architecture diagram.

The workflow uses multiple specialized agents:

1. Privacy and Safety Agent masks sensitive information.
2. Coordinator Agent orchestrates the workflow.
3. Career Path Comparator Agent scores multiple paths.
4. Skill Gap Agent identifies missing skills.
5. Roadmap Planner Agent creates the internship sprint.
6. Human Approval Agent lets the user review or adjust the recommendation before the final report.

This demonstrates a multi-agent system, security features, human-in-the-loop design, deployability, and an Agent Skill file.

## 1:30–2:15 — Demo Profile
Show the demo profile in the notebook.

The demo user is a 3rd-year B.Tech Computer Science student seeking an AI/ML internship. They know Python, basic machine learning, pandas, numpy, statistics, Git, scikit-learn, data preprocessing, and model evaluation. They have a student performance prediction project and want an internship in three months.

The resume text includes a sample email and phone number, so we can verify privacy masking.

## 2:15–3:20 — Run CareerCompass AI
Show the generated report.

First, the Privacy and Safety Agent masks the email and phone number.

Next, the system generates a Career Path Comparison Matrix. In this example, Machine Learning Intern receives the strongest Suitability Index, followed by Data Analyst Intern and Python Developer Intern.

The scoring is deterministic:
- 35% skill match
- 25% interest match
- 20% internship feasibility
- 10% project alignment
- 10% time readiness

Then the report explains why Machine Learning Intern was recommended, including matched skills and interest alignment. It also shows improvement areas like portfolio documentation, model deployment, and mock interview practice.

## 3:20–3:55 — Human Approval
Show Human-in-the-Loop section.

The Human Approval Agent is not just a checkbox. It can change the preferred career path, weekly time commitment, and internship deadline before the final roadmap is generated.

In this demo, the user approves Machine Learning Intern, increases weekly commitment to 12 hours, and changes the roadmap to 10 weeks. The final internship sprint reflects those changes.

## 3:55–4:25 — Evaluation / Validation
Show evaluation results.

The project includes three predefined evaluation profiles:
- AI/ML internship seeker
- Data analyst switcher
- Backend internship seeker

All pass their expected outcomes. The Kaggle reality check also verifies privacy masking, scoring, human approval, evaluation profiles, and optional ADK agent tree creation.

## 4:25–4:50 — Wrap-up / Future Work
CareerCompass AI demonstrates a complete multi-agent workflow that transforms a student profile into an explainable career comparison and personalized internship roadmap.

Future improvements include a guided Profile Completeness Agent, resume PDF parsing, job APIs, RAG over career resources, and a deployed UI.

Thank you.

# Recording Checklist

Show these on screen:

- [ ] GitHub repo
- [ ] Notebook roadmap
- [ ] Architecture diagram
- [ ] Demo profile
- [ ] Career comparison matrix
- [ ] Why recommendation section
- [ ] Human approval section
- [ ] Roadmap
- [ ] Evaluation PASS table
- [ ] Reality check passed

Keep final video under 5 minutes.
