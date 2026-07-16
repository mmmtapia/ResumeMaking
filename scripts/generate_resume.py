#!/usr/bin/env python3
"""Generate one tailored .docx resume from one profile."""
import argparse
from pathlib import Path

import yaml

from resume_lib import loader, filter as rfilter, docx_builder

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CAREER_DIR = REPO_ROOT / "career"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"

PROFILE_DEFAULTS = {
    "include_tags": None,
    "job_inclusion": "always",
    "include_jobs": [],
    "exclude_jobs": [],
    "max_bullets_per_job": None,
    "headline": None,
    "summary_override": None,
    "skills_categories": None,
    "education": "all",
    "certifications": "all",
    "awards": "all",
}


def load_profile(path: Path) -> dict:
    data = yaml.safe_load(path.read_text())
    for key, value in PROFILE_DEFAULTS.items():
        data.setdefault(key, value)
    return data


def generate(profile_path: Path, career_dir: Path = DEFAULT_CAREER_DIR,
             output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    profile = load_profile(profile_path)

    contact = loader.load_contact(career_dir)
    education = loader.load_education(career_dir)
    certifications = loader.load_certifications(career_dir)
    awards = loader.load_awards(career_dir)
    skills = loader.load_skills(career_dir)
    jobs = loader.load_jobs(career_dir)

    jobs_with_bullets = rfilter.select_jobs(jobs, profile)
    skill_categories = rfilter.select_skill_categories(skills, profile)
    selected_certifications = rfilter.select_certifications(certifications, profile)
    selected_education = rfilter.select_education(education, profile)
    selected_awards = rfilter.select_awards(awards, profile)

    doc = docx_builder.new_document()
    docx_builder.add_header(doc, contact)
    docx_builder.add_headline(doc, profile.get("headline"))
    summary = profile.get("summary_override") or contact.get("default_summary")
    docx_builder.add_summary(doc, summary)
    docx_builder.add_experience_section(doc, jobs_with_bullets)
    docx_builder.add_skills_section(doc, skill_categories)
    docx_builder.add_awards_section(doc, selected_awards)
    docx_builder.add_education_section(doc, selected_education)
    docx_builder.add_certifications_section(doc, selected_certifications)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / profile["output_filename"]
    doc.save(out_path)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path, help="Path to a profiles/*.yaml file")
    parser.add_argument("--career-dir", type=Path, default=DEFAULT_CAREER_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    out_path = generate(args.profile, args.career_dir, args.output_dir)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
