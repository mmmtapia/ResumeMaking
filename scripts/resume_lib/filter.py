"""Profile-driven selection of jobs, bullets, skills, education, certifications, awards."""


def select_bullets(job, profile):
    include_tags = profile.get("include_tags")
    max_bullets = profile.get("max_bullets_per_job")
    if include_tags is None:
        bullets = list(job.bullets)
    else:
        include_set = set(include_tags)
        bullets = [b for b in job.bullets if include_set & set(b.tags)]
    if max_bullets is not None:
        bullets = bullets[:max_bullets]
    return bullets


def _job_included(job, profile, matched_bullets):
    if job.id in profile.get("exclude_jobs", []):
        return False
    if job.id in profile.get("include_jobs", []):
        return True

    policy = profile.get("job_inclusion", "always")
    if policy == "always":
        return True
    if policy == "any_bullet_matches":
        return len(matched_bullets) > 0
    if policy == "job_tag_matches_or_any_bullet":
        include_tags = set(profile.get("include_tags") or [])
        return len(matched_bullets) > 0 or bool(include_tags & set(job.tags))
    raise ValueError(f"Unknown job_inclusion policy: {policy!r}")


def select_jobs(jobs, profile):
    """Returns a list of (job, bullets) tuples for jobs that should appear on the resume."""
    max_bullets = profile.get("max_bullets_per_job")

    result = []
    for job in jobs:
        matched = select_bullets(job, profile)
        if not _job_included(job, profile, matched):
            continue
        # A job can end up included with zero matching bullets via `include_jobs` (forced,
        # e.g. to avoid an employment gap) or `job_tag_matches_or_any_bullet` (job-level tag
        # matched but no bullet was tagged that granularly). Either way, a header with no
        # bullets under it is worse than showing the job's full bullet list.
        if not matched:
            matched = job.bullets[:max_bullets] if max_bullets is not None else list(job.bullets)
        result.append((job, matched))
    return result


def select_skill_categories(skills, profile):
    categories = skills.get("categories", [])
    selected = profile.get("skills_categories")
    if selected is None:
        include_tags = profile.get("include_tags")
        if include_tags is None:
            return categories
        include_set = set(include_tags)
        return [c for c in categories if include_set & set(c.get("tags", []))]
    selected_set = set(selected)
    return [c for c in categories if selected_set & set(c.get("tags", []))]


def _select_by_tag_policy(items, policy, include_tags):
    if policy == "none":
        return []
    if policy == "all":
        return list(items)
    if policy == "matching_tags":
        include_set = set(include_tags or [])
        return [i for i in items if include_set & set(i.get("tags", []))]
    raise ValueError(f"Unknown policy: {policy!r}")


def select_certifications(certifications, profile):
    return _select_by_tag_policy(
        certifications, profile.get("certifications", "all"), profile.get("include_tags")
    )


def select_awards(awards, profile):
    return _select_by_tag_policy(
        awards, profile.get("awards", "all"), profile.get("include_tags")
    )


def select_education(education, profile):
    mode = profile.get("education", "all")
    if mode == "all":
        return education
    if mode == "none":
        return []
    if isinstance(mode, list):
        return [e for e in education if e.get("institution") in mode]
    raise ValueError(f"Unknown education policy: {mode!r}")
