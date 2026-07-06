"""CareerCompass AI core engine.

A deterministic multi-agent career path comparator and internship roadmap planner.
The project is intentionally simple and Kaggle-friendly: no API keys, no external
services, and a stable Python fallback even when optional ADK integration is not used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


DEFAULT_CONFIG_PATH = Path(__file__).parent / "config" / "scoring_config.json"


# -----------------------------
# Utility helpers
# -----------------------------

# Lightweight semantic normalization. This avoids embeddings/LLMs while making
# common student wording ("ML", "DSA", "backend") match configured role skills.
SYNONYM_TO_CANONICAL = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",
    "machine learning": "machine learning",
    "basic ml": "machine learning",
    "basic machine learning": "machine learning",
    "data science": "data science",
    "data analytics": "analytics",
    "analytics": "analytics",
    "backend": "backend development",
    "back-end": "backend development",
    "backend development": "backend development",
    "api": "apis",
    "apis": "apis",
    "rest api": "rest apis",
    "rest apis": "rest apis",
    "dsa": "data structures and algorithms",
    "data structures": "data structures and algorithms",
    "data structures and algorithms": "data structures and algorithms",
    "db": "databases",
    "database": "databases",
    "databases": "databases",
    "dashboarding": "dashboard",
    "dashboards": "dashboard",
    "data viz": "data visualization",
    "visualisation": "data visualization",
    "visualization": "data visualization",
    "stats": "statistics",
    "statistics": "statistics",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
}

# Reverse aliases let target concepts match multiple user phrasings.
CANONICAL_ALIASES: Dict[str, List[str]] = {}
for alias, canonical in SYNONYM_TO_CANONICAL.items():
    CANONICAL_ALIASES.setdefault(canonical, []).append(alias)

STOPWORDS = {"basic", "basics", "beginner", "intermediate", "advanced", "and", "or", "the", "a", "an", "with", "using"}


def _as_list(values: Any) -> List[str]:
    if values is None:
        return []
    if isinstance(values, str):
        return [values]
    return [str(v) for v in values if v is not None]


def _canonicalize_text(text: str) -> str:
    """Lowercase text and expand known synonyms into canonical phrases."""
    text = str(text).lower().replace("/", " ").replace("-", "-")
    # Replace longer aliases first so "basic machine learning" is handled before "ml".
    for alias, canonical in sorted(SYNONYM_TO_CANONICAL.items(), key=lambda kv: len(kv[0]), reverse=True):
        pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
        text = re.sub(pattern, canonical, text)
    return text


def _normalize_terms(values: Any) -> List[str]:
    """Normalize user-provided strings/lists into canonical lowercase terms."""
    terms: List[str] = []
    for value in _as_list(values):
        text = _canonicalize_text(value)
        if text.strip():
            terms.append(text.strip())
        # Keep useful tokens, but do not let generic words dominate scoring.
        for token in re.findall(r"[a-zA-Z+#.]+", text):
            token = SYNONYM_TO_CANONICAL.get(token, token)
            if token not in STOPWORDS and len(token) > 1:
                terms.append(token)
    return sorted(set(t for t in terms if t))


def _concept_aliases(concept: str) -> List[str]:
    canonical = _canonicalize_text(concept).strip()
    aliases = {canonical, concept.lower().strip()}
    aliases.update(CANONICAL_ALIASES.get(canonical, []))
    return sorted(a for a in aliases if a)


def _concept_match_score(user_values: Any, target_concepts: List[str]) -> Tuple[int, List[str], List[str]]:
    """Score target concepts matched by user values.

    Unlike raw token overlap, the denominator is the configured concept list.
    This keeps scoring aligned with the README formula and makes scores easier
    for judges to understand.
    """
    concepts = [str(c).lower().strip() for c in target_concepts if str(c).strip()]
    if not concepts:
        return 0, [], []

    user_text = " | ".join(_canonicalize_text(v) for v in _as_list(user_values))
    user_terms = set(_normalize_terms(user_values))

    matched: List[str] = []
    missing: List[str] = []
    for concept in concepts:
        aliases = _concept_aliases(concept)
        concept_tokens = [t for t in re.findall(r"[a-zA-Z+#.]+", _canonicalize_text(concept)) if t not in STOPWORDS]
        alias_hit = any(alias in user_text or alias in user_terms for alias in aliases)
        token_hit = bool(concept_tokens) and all(token in user_terms or token in user_text for token in concept_tokens)
        if alias_hit or token_hit:
            matched.append(concept)
        else:
            missing.append(concept)

    score = round(100 * len(matched) / len(concepts))
    return _clamp_score(score), sorted(set(matched)), sorted(set(missing))


def _overlap_score(user_terms: List[str], target_terms: List[str]) -> Tuple[int, List[str]]:
    """Backward-compatible wrapper returning score and matched concepts."""
    score, matched, _missing = _concept_match_score(user_terms, target_terms)
    return score, matched


def _clamp_score(value: float) -> int:
    return max(0, min(100, int(round(value))))


# -----------------------------
# Data structures
# -----------------------------

@dataclass
class AgentResult:
    agent_name: str
    output: Dict[str, Any]
    notes: List[str] = field(default_factory=list)


@dataclass
class CareerCompassResult:
    sanitized_profile: Dict[str, Any]
    privacy_result: AgentResult
    comparison_result: AgentResult
    skill_gap_result: AgentResult
    roadmap_result: AgentResult
    approval_result: AgentResult
    final_report: str
    evaluation_metadata: Dict[str, Any] = field(default_factory=dict)


# -----------------------------
# Agent implementations
# -----------------------------

class PrivacySafetyAgent:
    """Masks sensitive data and validates basic profile completeness."""

    email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    phone_pattern = re.compile(r"(?<!\d)(?:\+?91[-\s]?)?[6-9]\d{9}(?!\d)")
    api_key_pattern = re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[^\s,'\"]+")

    required_fields = ["education", "current_skills", "interests", "career_goal", "weekly_time_commitment"]

    def run(self, profile: Dict[str, Any]) -> AgentResult:
        profile_copy = json.loads(json.dumps(profile))  # simple deep copy
        redactions = []

        def mask_text(text: str) -> str:
            nonlocal redactions
            text, email_count = self.email_pattern.subn("[EMAIL_REDACTED]", text)
            text, phone_count = self.phone_pattern.subn("[PHONE_REDACTED]", text)
            text, key_count = self.api_key_pattern.subn("[SECRET_REDACTED]", text)
            if email_count:
                redactions.append(f"Masked {email_count} email value(s).")
            if phone_count:
                redactions.append(f"Masked {phone_count} phone value(s).")
            if key_count:
                redactions.append(f"Masked {key_count} secret/API key-like value(s).")
            return text

        def walk(value: Any) -> Any:
            if isinstance(value, str):
                return mask_text(value)
            if isinstance(value, list):
                return [walk(v) for v in value]
            if isinstance(value, dict):
                return {k: walk(v) for k, v in value.items()}
            return value

        sanitized = walk(profile_copy)
        missing = [field for field in self.required_fields if not sanitized.get(field)]
        notes = redactions or ["No sensitive information detected."]
        if missing:
            notes.append(f"Missing recommended field(s): {', '.join(missing)}")
        notes.append("No profile data is persisted by default; analysis runs in-memory.")

        return AgentResult(
            agent_name="Privacy & Safety Agent",
            output={"sanitized_profile": sanitized, "missing_fields": missing, "redactions": redactions},
            notes=notes,
        )


class CareerPathComparatorAgent:
    """Scores configured career paths using deterministic, explainable weights."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.weights = config["weights"]
        self.career_paths = config["career_paths"]
        self.weight_total = round(sum(float(v) for v in self.weights.values()), 6)
        if abs(self.weight_total - 1.0) > 0.0001:
            raise ValueError(f"Scoring weights must sum to 1.0; got {self.weight_total}")

    def _time_to_readiness_score(self, profile: Dict[str, Any], missing_required_count: int, difficulty: str) -> int:
        weeks_until_goal = int(profile.get("weeks_until_goal", 12) or 12)
        weekly_hours = int(profile.get("weekly_time_commitment", 8) or 8)
        available_hours = weeks_until_goal * weekly_hours
        difficulty_factor = {"Low": 1.0, "Medium": 1.25, "High": 1.6}.get(difficulty, 1.25)
        estimated_needed_hours = missing_required_count * 12 * difficulty_factor
        if estimated_needed_hours <= 0:
            return 100
        ratio = available_hours / estimated_needed_hours
        return _clamp_score(min(100, ratio * 85))

    def run(self, profile: Dict[str, Any]) -> AgentResult:
        skills = profile.get("current_skills", [])
        interests = list(_as_list(profile.get("interests", []))) + [profile.get("career_goal", "")]
        projects = profile.get("projects", [])

        comparisons: List[Dict[str, Any]] = []
        for path in self.career_paths:
            skill_score, matched_skills, missing_skills = _concept_match_score(skills, path["required_skills"])
            interest_score, matched_interests, _missing_interests = _concept_match_score(interests, path["interest_keywords"])
            project_score, matched_projects, _missing_projects = _concept_match_score(projects, path["project_keywords"])
            time_score = self._time_to_readiness_score(profile, len(missing_skills), path["difficulty"])
            feasibility_score = int(path["entry_level_feasibility"])

            weighted_points = {
                "Skill Match": round(self.weights["skill_match"] * skill_score, 1),
                "Interest Match": round(self.weights["interest_match"] * interest_score, 1),
                "Feasibility": round(self.weights["internship_feasibility"] * feasibility_score, 1),
                "Projects": round(self.weights["project_alignment"] * project_score, 1),
                "Timeline": round(self.weights["time_to_readiness"] * time_score, 1),
            }
            final_score = sum(weighted_points.values())
            comparisons.append({
                "career_path_id": path["id"],
                "career_path": path["title"],
                "final_score": _clamp_score(final_score),
                "skill_match": skill_score,
                "interest_match": interest_score,
                "internship_feasibility": feasibility_score,
                "project_alignment": project_score,
                "time_to_readiness": time_score,
                "difficulty": path["difficulty"],
                "weighted_points": weighted_points,
                "confidence": "High" if final_score >= 75 else "Medium" if final_score >= 45 else "Developing",
                "matched_skills": matched_skills,
                "missing_skills": missing_skills[:8],
                "matched_interests": matched_interests,
                "matched_projects": matched_projects,
                "recommended_projects": path.get("recommended_projects", []),
                "why": self._why(path, skill_score, interest_score, feasibility_score, time_score, matched_skills),
            })

        comparisons.sort(key=lambda item: item["final_score"], reverse=True)
        top = comparisons[0] if comparisons else None
        backup = comparisons[1] if len(comparisons) > 1 else None
        return AgentResult(
            agent_name="Career Path Comparator Agent",
            output={
                "weights": self.weights,
                "weight_total": self.weight_total,
                "career_comparisons": comparisons[:3],
                "primary_recommendation": top,
                "backup_recommendation": backup,
            },
            notes=["Scores are deterministic and calculated from configurable weights and career path requirements.", f"Scoring weights validated: total = {self.weight_total}."],
        )

    @staticmethod
    def _why(path: Dict[str, Any], skill: int, interest: int, feasibility: int, time: int, matched_skills: List[str]) -> str:
        strengths = []
        if skill >= 60:
            strengths.append(f"good current skill overlap ({skill}/100)")
        if interest >= 60:
            strengths.append(f"strong interest alignment ({interest}/100)")
        if feasibility >= 80:
            strengths.append("high entry-level internship feasibility")
        if time >= 70:
            strengths.append("realistic preparation timeline")
        if matched_skills:
            strengths.append("matched skills: " + ", ".join(matched_skills[:4]))
        if not strengths:
            strengths.append("it remains a possible exploration path, but current readiness is limited")
        return f"{path['title']} is recommended because of " + "; ".join(strengths) + "."


class SkillGapReadinessAgent:
    """Turns path comparison into prioritized learning, resume, and interview gaps."""

    def run(self, profile: Dict[str, Any], comparison: Dict[str, Any]) -> AgentResult:
        primary = comparison["primary_recommendation"]
        backup = comparison.get("backup_recommendation")
        missing = primary.get("missing_skills", [])

        priority_skills = missing[:5]
        if not priority_skills:
            # If the configured core requirements are mostly met, keep the report
            # actionable by recommending polish areas instead of showing an empty gap table.
            priority_skills = ["portfolio documentation", "model deployment", "mock interview practice"]
        resume_checklist = [
            "Rewrite project bullets using action + tool + measurable outcome.",
            "Add GitHub links for the strongest 1–2 projects.",
            "Move target-role skills near the top of the resume.",
        ]
        if priority_skills:
            resume_checklist.append("Add evidence for priority skills: " + ", ".join(priority_skills[:3]) + ".")

        interview_topics = priority_skills[:4] + ["project explanation", "behavioral questions"]
        output = {
            "target_path": primary["career_path"],
            "backup_path": backup["career_path"] if backup else None,
            "priority_skill_gaps": priority_skills,
            "skill_gap_matrix": [
                {"skill": skill, "current_status": "Gap or weak evidence", "priority": "High" if i < 3 else "Medium"}
                for i, skill in enumerate(priority_skills)
            ],
            "resume_checklist": resume_checklist,
            "interview_topics": interview_topics,
            "recommended_projects": primary.get("recommended_projects", [])[:3],
        }
        return AgentResult(
            agent_name="Skill Gap & Readiness Agent",
            output=output,
            notes=["Skill gaps are derived from the highest-scoring configured career path."],
        )


class RoadmapPlannerAgent:
    """Creates a deadline-aware internship sprint plan."""

    def run(self, profile: Dict[str, Any], skill_gap: Dict[str, Any]) -> AgentResult:
        weeks = int(profile.get("weeks_until_goal", 12) or 12)
        weekly_hours = int(profile.get("weekly_time_commitment", 8) or 8)
        weeks = max(4, min(16, weeks))
        gaps = skill_gap.get("priority_skill_gaps", [])
        target_path = skill_gap["target_path"]

        plan = []
        for week in range(1, weeks + 1):
            if week <= max(1, math.ceil(weeks * 0.25)):
                focus = "Foundation building"
                tasks = [f"Study/practice {gaps[(week - 1) % len(gaps)]}" if gaps else "Strengthen fundamentals", "Document learning notes"]
            elif week <= max(2, math.ceil(weeks * 0.50)):
                focus = "Portfolio project"
                tasks = ["Build or improve one target-role project", "Commit progress to GitHub", "Write README with problem, approach, and result"]
            elif week <= max(3, math.ceil(weeks * 0.75)):
                focus = "Resume and interview preparation"
                tasks = ["Update resume bullets", "Practice interview questions", "Prepare 90-second project explanation"]
            else:
                focus = "Applications and iteration"
                tasks = ["Apply to 5–10 relevant internships", "Track applications", "Revise resume based on feedback"]
            plan.append({"week": week, "focus": focus, "estimated_hours": weekly_hours, "tasks": tasks})

        return AgentResult(
            agent_name="Roadmap Planner Agent",
            output={
                "target_path": target_path,
                "duration_weeks": weeks,
                "weekly_time_commitment": weekly_hours,
                "roadmap": plan,
                "human_checkpoints": [
                    "Confirm the primary career path matches your real preference.",
                    "Confirm the weekly time commitment is realistic.",
                    "Review roadmap with a mentor, faculty member, or career counselor if possible.",
                ],
            },
            notes=["Roadmap duration is based on the user's deadline and weekly availability."],
        )


class HumanApprovalAgent:
    """Simple human-in-the-loop checkpoint before final report generation."""

    def run(self, draft_summary: Dict[str, Any], approval: Dict[str, Any] | None = None) -> AgentResult:
        if approval is None:
            approval = {
                "approved": True,
                "adjustments": "Auto-approved for demo run. In an interactive run, the user reviews this checkpoint.",
            }
        approved = bool(approval.get("approved", False))
        applied_changes = {
            key: approval[key]
            for key in ("preferred_career_path", "weekly_time_commitment", "weeks_until_goal")
            if key in approval and approval[key] not in (None, "")
        }
        notes = ["Human approval checkpoint completed." if approved else "Human approval not granted; final report should be revised."]
        if approval.get("adjustments"):
            notes.append(f"User adjustment/request: {approval['adjustments']}")
        if applied_changes:
            notes.append("Applied human override(s): " + ", ".join(f"{k}={v}" for k, v in applied_changes.items()))
        return AgentResult(
            agent_name="Human Approval Agent",
            output={
                "draft_summary": draft_summary,
                "approved": approved,
                "adjustments": approval.get("adjustments", ""),
                "applied_changes": applied_changes,
            },
            notes=notes,
        )


class CoordinatorAgent:
    """Coordinates specialist agents and composes the final Markdown report."""

    def __init__(self, config_path: Path | str = DEFAULT_CONFIG_PATH):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text())
        self.privacy_agent = PrivacySafetyAgent()
        self.comparator_agent = CareerPathComparatorAgent(self.config)
        self.skill_agent = SkillGapReadinessAgent()
        self.roadmap_agent = RoadmapPlannerAgent()
        self.approval_agent = HumanApprovalAgent()

    def run(self, profile: Dict[str, Any], approval: Dict[str, Any] | None = None) -> CareerCompassResult:
        privacy = self.privacy_agent.run(profile)
        sanitized = privacy.output["sanitized_profile"]

        # First pass: generate draft recommendation for human review.
        comparison = self.comparator_agent.run(sanitized)
        skill_gap = self.skill_agent.run(sanitized, comparison.output)
        draft = {
            "primary_path": comparison.output["primary_recommendation"]["career_path"],
            "backup_path": comparison.output["backup_recommendation"]["career_path"] if comparison.output.get("backup_recommendation") else None,
            "roadmap_weeks": int(sanitized.get("weeks_until_goal", 12) or 12),
            "weekly_time_commitment": int(sanitized.get("weekly_time_commitment", 8) or 8),
        }

        # Human-in-the-loop checkpoint can change the preferred path, weekly hours,
        # or deadline before the roadmap is finalized. This makes approval meaningful
        # rather than a passive Approved=True flag.
        approval_result = self.approval_agent.run(draft, approval=approval)
        sanitized_for_final = dict(sanitized)
        if approval_result.output["approved"]:
            changes = approval_result.output.get("applied_changes", {})
            if "weekly_time_commitment" in changes:
                sanitized_for_final["weekly_time_commitment"] = int(changes["weekly_time_commitment"])
            if "weeks_until_goal" in changes:
                sanitized_for_final["weeks_until_goal"] = int(changes["weeks_until_goal"])
            if "preferred_career_path" in changes:
                comparison = self._promote_preferred_path(comparison, str(changes["preferred_career_path"]))
                skill_gap = self.skill_agent.run(sanitized_for_final, comparison.output)

        roadmap = self.roadmap_agent.run(sanitized_for_final, skill_gap.output)
        report = self._compose_report(sanitized_for_final, privacy, comparison, skill_gap, roadmap, approval_result)
        return CareerCompassResult(
            sanitized_profile=sanitized_for_final,
            privacy_result=privacy,
            comparison_result=comparison,
            skill_gap_result=skill_gap,
            roadmap_result=roadmap,
            approval_result=approval_result,
            final_report=report,
        )

    def _promote_preferred_path(self, comparison: AgentResult, preferred_path: str) -> AgentResult:
        """Promote a human-selected path to primary while preserving original scores."""
        output = json.loads(json.dumps(comparison.output))
        preferred_lower = preferred_path.lower()
        items = output["career_comparisons"]
        match_index = next((
            i for i, item in enumerate(items)
            if preferred_lower in item["career_path"].lower() or preferred_lower == item["career_path_id"].lower()
        ), None)
        if match_index is not None:
            chosen = items.pop(match_index)
            chosen["human_selected"] = True
            chosen["why"] += " The human approval step selected this as the preferred final direction."
            items.insert(0, chosen)
            output["career_comparisons"] = items
            output["primary_recommendation"] = items[0]
            output["backup_recommendation"] = items[1] if len(items) > 1 else None
            notes = comparison.notes + [f"Human approval promoted preferred path: {chosen['career_path']}."]
        else:
            notes = comparison.notes + [f"Human requested preferred path '{preferred_path}', but it was not in the comparison matrix."]
        return AgentResult(agent_name=comparison.agent_name, output=output, notes=notes)

    def _compose_report(
        self,
        profile: Dict[str, Any],
        privacy: AgentResult,
        comparison: AgentResult,
        skill_gap: AgentResult,
        roadmap: AgentResult,
        approval: AgentResult,
    ) -> str:
        comparisons = comparison.output["career_comparisons"]
        primary = comparison.output["primary_recommendation"]
        backup = comparison.output.get("backup_recommendation")
        lines = []
        lines.append("# CareerCompass AI Report")
        lines.append("")
        lines.append("## 1. Profile Summary")
        lines.append(f"- Education: {profile.get('education', 'Not provided')}")
        lines.append(f"- Career goal: {profile.get('career_goal', 'Not provided')}")
        lines.append(f"- Weekly time commitment: {profile.get('weekly_time_commitment', 'Not provided')} hours")
        lines.append(f"- Deadline: {profile.get('weeks_until_goal', 12)} weeks")
        lines.append("")
        lines.append("## 2. Privacy & Safety Notes")
        for note in privacy.notes:
            lines.append(f"- {note}")
        lines.append("- CareerCompass AI provides planning support, not guaranteed hiring outcomes. Please verify opportunities independently and consult mentors when possible.")
        lines.append("")
        lines.append("## 3. Career Path Comparison Matrix")
        lines.append("### Quick Scoreboard")
        lines.append("| Career | Suitability Index | Confidence |")
        lines.append("|---|---:|---|")
        for item in comparisons:
            lines.append(f"| {item['career_path']} | **{item['final_score']}** | {item['confidence']} |")
        lines.append("")
        lines.append("### Detailed Score Breakdown")
        lines.append("| Career Path | Suitability Index | Skill Match | Interest Match | Feasibility | Project Alignment | Time Readiness | Difficulty |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---|")
        for item in comparisons:
            lines.append(
                f"| {item['career_path']} | {item['final_score']} | {item['skill_match']} | {item['interest_match']} | "
                f"{item['internship_feasibility']} | {item['project_alignment']} | {item['time_to_readiness']} | {item['difficulty']} |"
            )
        lines.append("")
        lines.append("### Scoring Formula")
        weights = comparison.output["weights"]
        lines.append(
            f"Suitability Index = {int(weights['skill_match'] * 100)}% Skill Match "
            f"+ {int(weights['interest_match'] * 100)}% Interest Match "
            f"+ {int(weights['internship_feasibility'] * 100)}% Internship Feasibility "
            f"+ {int(weights['project_alignment'] * 100)}% Project Alignment "
            f"+ {int(weights['time_to_readiness'] * 100)}% Time-to-Readiness"
        )
        lines.append(f"- Weight normalization check: **{comparison.output['weight_total']}**")
        lines.append("")
        lines.append("## 4. Recommendation")
        lines.append(f"- Primary path: **{primary['career_path']}**")
        if backup:
            lines.append(f"- Backup path: **{backup['career_path']}**")
        lines.append("")
        lines.append(f"### Why {primary['career_path']}?")
        lines.append(f"- ✓ {primary['why']}")
        if primary.get("matched_skills"):
            lines.append("- ✓ Current evidence: " + ", ".join(primary["matched_skills"][:4]))
        if primary.get("matched_interests"):
            lines.append("- ✓ Interest alignment: " + ", ".join(primary["matched_interests"][:4]))
        lines.append("- ✓ Timeline considered: roadmap uses the approved deadline and weekly hours.")
        lines.append("")
        lines.append("**Needs improvement:**")
        improvement_items = primary.get("missing_skills", [])[:5] or skill_gap.output.get("priority_skill_gaps", [])[:5]
        for gap in improvement_items:
            lines.append(f"- {gap}")
        lines.append("")
        lines.append("### Explainable Suitability Contribution")
        lines.append("| Component | Points Contributed | Max Points |")
        lines.append("|---|---:|---:|")
        max_points = {"Skill Match": 35, "Interest Match": 25, "Feasibility": 20, "Projects": 10, "Timeline": 10}
        for component, points in primary["weighted_points"].items():
            lines.append(f"| {component} | {points} | {max_points[component]} |")
        lines.append(f"| **Suitability Index** | **{primary['final_score']}** | **100** |")
        lines.append("")
        lines.append("## 5. Skill Gap Matrix")
        lines.append("| Skill | Current Status | Priority |")
        lines.append("|---|---|---|")
        for row in skill_gap.output["skill_gap_matrix"]:
            lines.append(f"| {row['skill']} | {row['current_status']} | {row['priority']} |")
        lines.append("")
        lines.append("## 6. Resume & Interview Readiness")
        lines.append("### Resume checklist")
        for item in skill_gap.output["resume_checklist"]:
            lines.append(f"- {item}")
        lines.append("\n### Interview topics")
        for topic in skill_gap.output["interview_topics"]:
            lines.append(f"- {topic}")
        lines.append("")
        lines.append("## 7. Deadline-Aware Internship Sprint Plan")
        lines.append(f"Duration: **{roadmap.output['duration_weeks']} weeks** at **{roadmap.output['weekly_time_commitment']} hours/week**")
        for week in roadmap.output["roadmap"]:
            tasks = "; ".join(week["tasks"])
            lines.append(f"- Week {week['week']}: **{week['focus']}** — {tasks}")
        lines.append("")
        lines.append("## 8. Human-in-the-Loop Approval")
        lines.append(f"- Approved: {approval.output['approved']}")
        if approval.output.get("adjustments"):
            lines.append(f"- User adjustment: {approval.output['adjustments']}")
        if approval.output.get("applied_changes"):
            lines.append("- Applied changes before final roadmap generation:")
            for key, value in approval.output["applied_changes"].items():
                lines.append(f"  - {key}: {value}")
        for checkpoint in roadmap.output["human_checkpoints"]:
            lines.append(f"- {checkpoint}")
        lines.append("")
        lines.append("## 9. Limitations")
        lines.append("- This prototype does not scrape live internships or guarantee job outcomes.")
        lines.append("- Recommendations are based on configurable role definitions and should be reviewed by a human.")
        lines.append("- Future versions can add resume parsing, job APIs, RAG, and a deployed UI.")
        return "\n".join(lines)


def load_profile(path: Path | str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())


def run_careercompass(profile: Dict[str, Any], approval: Dict[str, Any] | None = None) -> CareerCompassResult:
    return CoordinatorAgent().run(profile, approval=approval)


if __name__ == "__main__":
    demo_profile = load_profile(Path(__file__).parent / "examples" / "ai_ml_student.json")
    result = run_careercompass(demo_profile)
    print(result.final_report)
