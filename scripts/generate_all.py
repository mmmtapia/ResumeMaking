#!/usr/bin/env python3
"""Generate a .docx resume for every profile in profiles/*.yaml.

Adding a new tailored resume never requires touching this file -- just add
a new profiles/<name>.yaml.
"""
from pathlib import Path

from generate_resume import generate, DEFAULT_CAREER_DIR, DEFAULT_OUTPUT_DIR

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = REPO_ROOT / "profiles"


def main() -> None:
    profile_paths = sorted(PROFILES_DIR.glob("*.yaml"))
    if not profile_paths:
        print(f"No profiles found in {PROFILES_DIR}")
        return
    for profile_path in profile_paths:
        out_path = generate(profile_path, DEFAULT_CAREER_DIR, DEFAULT_OUTPUT_DIR)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
