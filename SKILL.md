---
name: career-roadmap
description: >-
  Use this skill when asked to compare career paths, identify student skill gaps,
  create internship preparation roadmaps, or review career recommendations for
  university students and early-career professionals. The skill emphasizes
  explainable scoring, privacy protection, and human-in-the-loop review.
---

# Career Roadmap Skill

## Purpose

Create a personalized career and internship planning report that is structured,
explainable, privacy-conscious, and suitable for human review.

## When to Use

Use this skill when the user asks for:

- career path comparison
- internship planning
- student skill gap analysis
- semester or week-by-week preparation roadmap
- resume or interview readiness planning
- explanation of why a career recommendation was made

## Required Inputs

Collect or infer the following fields when available:

1. Education and current year/status
2. Current skills
3. Interests
4. Projects or experience
5. Career goal
6. Weekly time commitment
7. Deadline or weeks until internship/job target
8. Preferred location or remote preference, if relevant

## Procedure

1. **Protect privacy first**
   - Mask emails, phone numbers, API keys, or unnecessary personal identifiers.
   - Do not persist personal data unless the user explicitly asks.

2. **Compare career paths**
   - Recommend multiple possible paths, not just one.
   - Score each path using transparent criteria:
     - Skill Match
     - Interest Match
     - Internship Feasibility
     - Project Alignment
     - Time-to-Readiness

3. **Explain the recommendation**
   - Include a brief "Why this recommendation?" section.
   - Mention matched skills, interests, feasibility, and preparation timeline.

4. **Identify skill gaps**
   - Prioritize gaps that affect internship readiness.
   - Keep the list small and actionable.

5. **Create a deadline-aware roadmap**
   - Use the user's available weeks and weekly hours.
   - Divide work into foundation, portfolio, resume/interview, and applications.

6. **Add human-in-the-loop approval**
   - Ask the user to confirm the primary path and time commitment before finalizing.
   - Include any user adjustments in the final report.

7. **End with limitations**
   - Do not guarantee jobs or internships.
   - Encourage users to verify opportunities and consult mentors.

## Output Format

Return a structured report with these sections:

1. Profile Summary
2. Privacy & Safety Notes
3. Career Path Comparison Matrix
4. Recommendation
5. Why this recommendation?
6. Skill Gap Matrix
7. Resume & Interview Readiness
8. Deadline-Aware Internship Sprint Plan
9. Human-in-the-Loop Approval
10. Limitations and Future Work

## Quality Checklist

Before finishing, verify:

- [ ] At least two or three career paths were compared.
- [ ] Scores are explainable.
- [ ] Sensitive information is masked.
- [ ] The roadmap respects the user's deadline and weekly availability.
- [ ] A human approval checkpoint is included.
- [ ] The output is not generic chatbot advice.
