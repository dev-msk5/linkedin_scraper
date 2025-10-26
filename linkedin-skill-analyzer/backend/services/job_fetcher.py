import json
import os

from typing import List, Dict


DEFAULT_SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_jobs.json")


def load_sample_jobs(path: str | None = None, scale: int = 1) -> List[Dict]:
    """Load sample job listings from a JSON file.

    Args:
        path: Optional path to a JSON file. If not provided, uses the default
            `backend/data/sample_jobs.json` relative to this module.
        scale: If >1, duplicate and slightly vary the loaded jobs to simulate
            a larger dataset for testing. This does not change the on-disk file.

    Returns:
        List of job dictionaries. Each job dict should contain at minimum
        'title' and 'description' keys. If loading fails, returns an empty list.
    """
    if path is None:
        # normalize path (relative to package)
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "sample_jobs.json"))

    base_jobs: List[Dict] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                base_jobs = data
            # If file has top-level object with `jobs` key, accept that too
            elif isinstance(data, dict) and "jobs" in data and isinstance(data["jobs"], list):
                base_jobs = data["jobs"]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if scale <= 1 or not base_jobs:
        return base_jobs

    # Expand the dataset by repeating base jobs with small variations
    scaled: List[Dict] = []
    n = len(base_jobs)
    for i in range(scale * n):
        src = base_jobs[i % n].copy()
        # Add a small suffix to make titles/companies slightly unique for realism
        suffix = f" (sample {i})"
        if "title" in src and src["title"]:
            src["title"] = src["title"] + suffix
        if "company" in src and src["company"]:
            src["company"] = src["company"] + suffix
        # Optionally tweak location or description minimally
        if "location" in src and src["location"]:
            src["location"] = src["location"]
        scaled.append(src)

    return scaled


if __name__ == "__main__":
    # Quick manual test
    jobs = load_sample_jobs()
    print(f"Loaded {len(jobs)} sample jobs")
