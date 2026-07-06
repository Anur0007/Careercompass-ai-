"""Final clean run check for pre-submission verification.

Required checks must pass. Optional ADK may fail in environments where google-adk
is not installed; the deterministic fallback remains the submission-safe path.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

REQUIRED_COMMANDS = [
    [sys.executable, "careercompass.py"],
    [sys.executable, "evaluate_profiles.py"],
    [sys.executable, "kaggle_reality_check.py"],
]

OPTIONAL_COMMANDS = [
    [sys.executable, "adk_app.py"],
]


def _run(cmd, required=True):
    print(f"\n$ {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=30)
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr)
    if completed.returncode != 0 and required:
        raise SystemExit(f"Required command failed: {' '.join(cmd)}")
    if completed.returncode != 0:
        print(f"OPTIONAL CHECK WARNING: {' '.join(cmd)} failed, but deterministic fallback is valid.")
    return completed.returncode == 0


def main():
    for cmd in REQUIRED_COMMANDS:
        _run(cmd, required=True)

    optional_results = [_run(cmd, required=False) for cmd in OPTIONAL_COMMANDS]

    print("\nCLEAN RUN CHECK PASSED")
    if not all(optional_results):
        print("Optional ADK did not run in this environment. This is acceptable if the fallback deterministic engine passes.")


if __name__ == "__main__":
    main()
