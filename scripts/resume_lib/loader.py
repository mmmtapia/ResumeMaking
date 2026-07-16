"""Load career/*.yaml into plain data structures."""
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Bullet:
    text: str
    tags: list


@dataclass
class Job:
    id: str
    employer: str
    title: str
    location: str
    start_date: str
    end_date: str
    tags: list
    bullets: list
    skills: list


def _read_yaml(path: Path, default=None):
    if not path.exists():
        return default
    return yaml.safe_load(path.read_text()) or default


def load_contact(career_dir: Path) -> dict:
    return _read_yaml(career_dir / "contact.yaml", default={})


def load_education(career_dir: Path) -> list:
    return _read_yaml(career_dir / "education.yaml", default=[])


def load_certifications(career_dir: Path) -> list:
    return _read_yaml(career_dir / "certifications.yaml", default=[])


def load_awards(career_dir: Path) -> list:
    return _read_yaml(career_dir / "awards.yaml", default=[])


def load_skills(career_dir: Path) -> dict:
    return _read_yaml(career_dir / "skills.yaml", default={"categories": []})


def _job_sort_key(job: Job):
    if job.end_date == "present":
        return 9999
    return int(job.end_date)


def load_jobs(career_dir: Path) -> list:
    jobs_dir = career_dir / "jobs"
    jobs = []
    seen_ids = set()
    for path in sorted(jobs_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        if data["id"] in seen_ids:
            raise ValueError(f"Duplicate job id {data['id']!r} in {path}")
        seen_ids.add(data["id"])
        bullets = [
            Bullet(text=b["text"], tags=b.get("tags", []))
            for b in data.get("bullets", [])
        ]
        jobs.append(Job(
            id=data["id"],
            employer=data["employer"],
            title=data["title"],
            location=data.get("location", ""),
            start_date=str(data["start_date"]),
            end_date=str(data["end_date"]),
            tags=data.get("tags", []),
            bullets=bullets,
            skills=data.get("skills", []),
        ))
    return sorted(jobs, key=_job_sort_key, reverse=True)
