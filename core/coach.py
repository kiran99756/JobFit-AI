import os

import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "You are a concise, practical career coach helping someone tailor their "
    "resume and prep for a specific job. Be direct and specific to the resume "
    "and job description given — avoid generic advice. Keep the response under "
    "300 words, using short paragraphs or bullet points."
)


class CoachError(Exception):
    pass


def get_career_advice(resume_text, job_description, score, matched, missing):
    """Calls the Groq API for personalized career coaching advice.
    Raises CoachError with a user-facing message on any failure."""

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise CoachError(
            "No GROQ_API_KEY found. Set it as an environment variable, or add "
            "it to a local .env file (see .env.example) before using the "
            "AI Career Coach."
        )

    user_prompt = f"""
Resume:
{resume_text[:4000]}

Job description:
{job_description[:2000]}

ATS match score: {score}%
Matched skills: {', '.join(matched) if matched else 'none'}
Missing skills: {', '.join(missing) if missing else 'none'}

Give this candidate specific, actionable coaching for landing this role:
what to emphasize, what to fix, and how to talk about the missing skills
if asked in an interview.
""".strip()

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.6,
        "max_tokens": 500,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    except requests.RequestException as e:
        raise CoachError(f"Could not reach Groq API: {e}")

    if response.status_code == 401:
        raise CoachError("Groq API rejected the key (401 Unauthorized). Check GROQ_API_KEY.")
    if response.status_code == 429:
        raise CoachError("Groq API rate limit hit (429). Try again in a moment.")
    if response.status_code != 200:
        raise CoachError(f"Groq API error {response.status_code}: {response.text[:300]}")

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise CoachError("Unexpected response format from Groq API.")
