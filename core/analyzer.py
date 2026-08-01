import re

from core.skills import SKILLS


def _contains_skill(text, skill):
    """Word-boundary match so short skills like 'c' or 'ai' don't false-positive
    on substrings inside other words (e.g. 'c' inside 'react')."""
    pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def analyze_resume(resume_text, job_description):

    resume = resume_text.lower()
    job = job_description.lower()

    matched = []
    missing = []

    for skill in SKILLS:

        if _contains_skill(job, skill):

            if _contains_skill(resume, skill):
                matched.append(skill)
            else:
                missing.append(skill)

    total = len(matched) + len(missing)

    if total == 0:
        score = 0
    else:
        score = int((len(matched) / total) * 100)

    return score, matched, missing