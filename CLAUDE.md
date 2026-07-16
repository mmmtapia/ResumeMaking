# ResumeMaking

Maintains a single structured career history and generates multiple tailored
`.docx` resumes from it (e.g. a full resume, a Mission Assurance resume, a
Systems Engineering resume) driven by config files, so a new tailored resume
never requires code changes.

## Python virtual environment is mandatory

Every Python command in this repo — running scripts, installing packages —
must go through the project's `.venv`, never the system/global Python.

```
source .venv/bin/activate      # once per shell session
python3 scripts/generate_all.py
```

or invoke the interpreter directly without activating:

```
.venv/bin/python3 scripts/generate_all.py
```

If `.venv` doesn't exist yet, create it before doing anything else:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Never run `pip install` or a script with the bare `python3`/`pip3` from
outside `.venv`.

## Directory map

- `career/` — the source of truth. `career/jobs/*.yaml` (one file per job),
  plus `contact.yaml`, `education.yaml`, `certifications.yaml`, `skills.yaml`.
- `profiles/` — one YAML file per tailored resume, declaring which tags to
  include and how to render them. Adding a new tailored resume = adding a
  new file here; `generate_all.py` picks it up automatically.
- `templates/resume_style.docx` — style-only Word doc (fonts, margins,
  heading styles). All generated resumes load this for consistent look;
  don't hand-roll formatting per profile.
- `scripts/` — `generate_resume.py` (one profile → one `.docx`),
  `generate_all.py` (all profiles → all `.docx`), `convert_intake.py`
  (drop-folder files → plain text), `resume_lib/` (shared loader/filter/
  docx-building code).
- `intake/drop/` — drop any source file here (old resume, LinkedIn export,
  etc.) as raw input. `intake/converted/` holds the plain-text conversions;
  both are gitignored (personal data, not source of truth).
- `output/` — generated `.docx` resumes; gitignored.
- `.claude/skills/` — reserved for future custom Claude Code skills for this
  project; empty for now.

## How to add a new job

Create `career/jobs/<start_YYYY-MM>_<employer-slug>.yaml` following the
existing schema (see any file in that directory for the shape). Give every
bullet a `text` and a `tags` list — tags are what tailored resumes filter on,
so an untagged bullet will never appear on a tailored (non-full) resume.

## How to add a new tailored resume

Add `profiles/<name>.yaml`. No code changes are needed — `generate_all.py`
globs `profiles/*.yaml`. See existing profiles for the available fields
(`include_tags`, `job_inclusion`, `max_bullets_per_job`, `headline`, etc.).

## Tag taxonomy

Reuse existing tags instead of inventing near-duplicates. Current tags in
use (check `career/jobs/*.yaml` and `career/skills.yaml` for the live list
as it grows): `mission-assurance`, `systems-engineering`, `leadership`.
Verification and architecture work are tagged `systems-engineering` rather
than split into their own tags.

## Intake is manual, not auto-parsed

`convert_intake.py` only converts a dropped file to plain text — it does
**not** attempt to parse that text into structured job entries. Turning
resume prose into correctly-tagged `career/jobs/*.yaml` bullets is a
judgment call (matching text to the right job, deduplicating, choosing
tags, tightening wording) and is done collaboratively, by hand, using the
converted text as reference. Do not build a regex/NLP auto-parser for this
— it would silently produce wrong structured data.

## Commands reference

```
python3 scripts/generate_resume.py --profile profiles/mission-assurance.yaml
python3 scripts/generate_all.py
python3 scripts/convert_intake.py
```

## Personal data

`career/*.yaml` contains real personal/employment data and is tracked in
git — treat this repository as private. `intake/drop/`, `intake/converted/`,
and `output/*.docx` are gitignored for the same reason.
