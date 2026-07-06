"""Small evaluation harness for CareerCompass AI."""
from pathlib import Path
from careercompass import CoordinatorAgent, load_profile

TESTS = [
    ("AI/ML Internship Seeker", "examples/ai_ml_student.json", ["Data Analyst Intern", "Machine Learning Intern"]),
    ("Data Analyst Switcher", "examples/data_analyst_switcher.json", ["Data Analyst Intern", "Business Analyst Intern"]),
    ("Backend Intern", "examples/backend_intern.json", ["Backend Developer Intern", "Python Developer Intern"]),
]

def main():
    root = Path(__file__).parent
    agent = CoordinatorAgent(root / "config" / "scoring_config.json")
    print("| Test Profile | Expected Primary Output | Observed Primary Output | Pass/Fail |")
    print("|---|---|---|---|")
    for name, rel_path, expected_any in TESTS:
        profile = load_profile(root / rel_path)
        result = agent.run(profile)
        observed = result.comparison_result.output["primary_recommendation"]["career_path"]
        passed = observed in expected_any
        print(f"| {name} | {' or '.join(expected_any)} | {observed} | {'PASS' if passed else 'REVIEW'} |")

if __name__ == "__main__":
    main()
