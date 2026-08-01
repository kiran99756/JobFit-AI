import re


ACTION_VERBS = [
    "led", "built", "developed", "designed", "implemented", "created",
    "managed", "optimized", "launched", "automated", "improved",
    "reduced", "increased", "delivered", "architected"
]

SECTIONS = ["experience", "education", "project", "skill"]


def generate_suggestions(resume_text, matched, missing, score):
    """Generate suggestions dynamically from the actual resume content
    and analysis results, instead of a static hardcoded list."""

    resume_lower = resume_text.lower()
    suggestions = []

    # 1. Missing skills relevant to this job
    if missing:
        top_missing = missing[:5]
        suggestions.append(
            f"Add these in-demand skills if you have real experience with them: "
            f"{', '.join(top_missing)}."
        )

    # 2. Quantifiable achievements
    has_numbers = bool(re.search(r"\d+%|\$\d+|\b\d+\+?\b", resume_lower))
    if not has_numbers:
        suggestions.append(
            "Add measurable achievements (e.g. 'reduced load time by 30%', "
            "'led a team of 5') — numbers make impact concrete to recruiters and ATS."
        )

    # 3. Action verbs
    verb_count = sum(1 for v in ACTION_VERBS if v in resume_lower)
    if verb_count < 3:
        suggestions.append(
            "Start more bullet points with strong action verbs "
            "(e.g. 'led', 'built', 'optimized') instead of passive phrasing."
        )

    # 4. Contact info
    if "@" not in resume_text:
        suggestions.append(
            "Make sure a professional email address is clearly visible on the resume."
        )

    # 5. Length check
    word_count = len(resume_text.split())
    if word_count < 150:
        suggestions.append(
            "The resume looks quite short — consider expanding on projects, "
            "responsibilities, and outcomes."
        )
    elif word_count > 1100:
        suggestions.append(
            "The resume is on the longer side — aim to trim it to 1-2 pages "
            "for easier scanning."
        )

    # 6. Missing standard sections
    missing_sections = [s for s in SECTIONS if s not in resume_lower]
    for section in missing_sections:
        suggestions.append(f"Consider adding a clearly labeled '{section.capitalize()}' section.")

    # 7. Score-based closing note
    if score < 40:
        suggestions.append(
            "The ATS score is low for this job — rework the resume to mirror "
            "more of the job description's specific keywords and phrasing."
        )
    elif score >= 80:
        suggestions.append(
            "Strong match for this role — the resume already reflects most of "
            "the key skills the job description asks for."
        )

    if not suggestions:
        suggestions.append("The resume looks well-aligned with this job description.")

    return suggestions
