from flask import Blueprint, request, jsonify

# Try imports that work both when running from project root and when running
# the backend package as a module.
try:
    from backend.services import job_fetcher, skill_extractor
except Exception:
    try:
        # When cwd is backend/ this import should work
        from services import job_fetcher, skill_extractor
    except Exception:
        # As a last resort, try a relative import (may fail when executed as script)
        from ..services import job_fetcher, skill_extractor  # type: ignore
try:
    from backend.utils import text_cleaner
except Exception:
    try:
        from utils import text_cleaner
    except Exception:
        from ..utils import text_cleaner  # type: ignore


api_bp = Blueprint("api", __name__)


@api_bp.route("/skills")
def api_skills():
    """Fetch jobs, optionally filter by role, extract skills and return frequencies.

    Query params:
      - role: optional role string to filter jobs (e.g. 'data analyst')

    Response JSON:
      {
        "role": <string or null>,
        "job_count": <int>,
        "skills": { <skill>: <count>, ... }
      }
    """
    role = request.args.get("role", "").strip()

    # Load jobs from the job_fetcher service. Accept an optional `scale` query
    # parameter for testing large datasets (e.g. scale=100 will produce many
    # entries by duplicating the sample jobs).
    scale = 1
    try:
        scale = int(request.args.get("scale", "1"))
        if scale < 1:
            scale = 1
    except ValueError:
        scale = 1

    jobs = job_fetcher.load_sample_jobs(scale=scale)

    if role:
        # Use tokenized, normalized matching to improve recall (e.g. 'software developer intern'
        # should match jobs containing 'developer'). We fall back to substring matching if
        # tokenization yields no hits.
        role_tokens = set(text_cleaner.clean_text(role))
        filtered = []
        for j in jobs:
            title = (j.get("title") or "")
            desc = (j.get("description") or "")
            # Build a token set for the job (title + description)
            job_tokens = set(text_cleaner.clean_text(f"{title} {desc}"))

            # If any overlap, include the job
            if role_tokens & job_tokens:
                filtered.append(j)
            else:
                # fallback: substring match (case-insensitive)
                rl = role.lower()
                if rl in title.lower() or rl in desc.lower():
                    filtered.append(j)

        jobs_to_use = filtered
    else:
        jobs_to_use = jobs

    skills_freq = skill_extractor.extract_skills(jobs_to_use)

    return jsonify({"role": role or None, "job_count": len(jobs_to_use), "skills": skills_freq})
