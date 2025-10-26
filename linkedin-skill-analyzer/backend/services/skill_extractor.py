import re
from typing import List, Dict


DEFAULT_SKILLS = [
    "python",
    "machine learning",
    "pandas",
    "sql",
    "javascript",
    "react",
    "css",
    "communication",
    "stakeholder",
    "roadmapping",
]


def extract_skills(jobs: List[Dict], skills_list: List[str] | None = None) -> Dict[str, int]:
    """Very small mock skill extractor.

    Scans `title` and `description` fields of each job looking for keywords from
    `skills_list` and returns a dict of skill -> frequency.

    This is intentionally simplistic and meant as a placeholder for later NLP.
    """
    if skills_list is None:
        skills_list = DEFAULT_SKILLS

    # compile regexes for each skill for a case-insensitive search
    patterns = {skill: re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE) for skill in skills_list}

    counts: Dict[str, int] = {skill: 0 for skill in skills_list}

    for job in jobs:
        text = ""
        if isinstance(job, dict):
            title = job.get("title", "") or ""
            desc = job.get("description", "") or ""
            text = f"{title}\n{desc}"

        for skill, pat in patterns.items():
            if pat.search(text):
                counts[skill] += 1

    # Remove zero-count skills for a cleaner output
    return {s: c for s, c in counts.items() if c > 0}


if __name__ == "__main__":
    # quick smoke test
    sample = [
        {"title": "Data Scientist", "description": "Experience in Python, pandas and SQL."},
        {"title": "Frontend Developer", "description": "Strong JavaScript and React skills."},
    ]
    print(extract_skills(sample))
