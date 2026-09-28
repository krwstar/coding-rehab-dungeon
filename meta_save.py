import json

from pathlib import Path


SAVE_FILE = Path("meta_save.json")

REQUIRED_JOBS = {
    "전사",
    "마법사",
    "도적",
    "수호자",
    "검객",
}

DEFAULT_SAVE = {
    "cleared_jobs": [],
}


def load_meta_save():
    if not SAVE_FILE.exists():
        return DEFAULT_SAVE.copy()

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return DEFAULT_SAVE.copy()

        if not isinstance(data.get("cleared_jobs"), list):
            data["cleared_jobs"] = []

        return data

    except (
        OSError,
        json.JSONDecodeError,
    ):
        return DEFAULT_SAVE.copy()


def save_meta_save(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4,
            )

        return True

    except OSError:
        return False


def register_job_clear(job):
    if job not in REQUIRED_JOBS:
        return False

    data = load_meta_save()
    cleared_jobs = data["cleared_jobs"]

    if job in cleared_jobs:
        return False

    cleared_jobs.append(job)
    return save_meta_save(data)


def all_jobs_cleared():
    data = load_meta_save()
    cleared_jobs = set(data["cleared_jobs"])

    return REQUIRED_JOBS.issubset(cleared_jobs)