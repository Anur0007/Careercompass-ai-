"""Reality check for Kaggle submission readiness.
Run this before documentation/video work:
    python kaggle_reality_check.py
"""
from pathlib import Path
import json

from careercompass import CoordinatorAgent, load_profile, run_careercompass
from evaluate_profiles import TESTS

ROOT = Path(__file__).parent


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"✅ {message}")


def main():
    print("CAREERCOMPASS AI — KAGGLE REALITY CHECK")
    print("=" * 52)

    # 1. Core demo profile
    profile = load_profile(ROOT / "examples" / "ai_ml_student.json")
    approval = {
        "approved": True,
        "preferred_career_path": "Machine Learning Intern",
        "weekly_time_commitment": 12,
        "weeks_until_goal": 10,
        "adjustments": "Reality-check approval: keep ML target and regenerate a 10-week roadmap.",
    }
    result = run_careercompass(profile, approval=approval)
    primary = result.comparison_result.output["primary_recommendation"]

    assert_true(primary["career_path"] == "Machine Learning Intern", "Main profile primary path is Machine Learning Intern")
    assert_true(primary["final_score"] >= 70, "Main profile Suitability Index is presentation-safe (>=70)")
    assert_true(result.roadmap_result.output["duration_weeks"] == 10, "Human approval changed deadline to 10 weeks")
    assert_true(result.roadmap_result.output["weekly_time_commitment"] == 12, "Human approval changed weekly time to 12 hours")
    assert_true("[EMAIL_REDACTED]" in json.dumps(result.sanitized_profile), "Email masking works")
    assert_true("[PHONE_REDACTED]" in json.dumps(result.sanitized_profile), "Phone masking works")
    assert_true("Suitability Index" in result.final_report, "Final report uses Suitability Index wording")
    assert_true("Why Machine Learning Intern?" in result.final_report, "Final report includes bullet-style recommendation explanation")

    # 2. Evaluation profiles
    agent = CoordinatorAgent(ROOT / "config" / "scoring_config.json")
    for name, rel_path, expected_any in TESTS:
        test_profile = load_profile(ROOT / rel_path)
        test_result = agent.run(test_profile)
        observed = test_result.comparison_result.output["primary_recommendation"]["career_path"]
        assert_true(observed in expected_any, f"Evaluation profile '{name}' matches expectation: {observed}")

    # 3. Optional ADK import/tree check
    try:
        from adk_app import build_adk_agent_tree
        tree = build_adk_agent_tree()
        assert_true(len(tree.sub_agents) == 5, "Optional Google ADK agent tree builds with 5 sub-agents")
    except Exception as exc:
        print(f"⚠️ Optional ADK check failed, fallback deterministic engine is still working: {exc}")

    print("=" * 52)
    print("✅ REALITY CHECK PASSED")


if __name__ == "__main__":
    main()
