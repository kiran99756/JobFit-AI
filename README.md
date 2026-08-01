# JobFit AI

Resume vs. job description analyzer — desktop app (CustomTkinter).

## Setup

```
pip install -r requirements.txt
python main.py
```

## Features

- **ATS Score** — % of the job description's key skills found in your resume
- **Skill Matching** — matched vs. missing skills, with word-boundary matching
  (fixed a bug where short skills like "c" or "ai" were false-positive
  matching inside other words, e.g. "c" inside "react")
- **Resume Suggestions** — generated dynamically from your actual resume text
  (checks for quantifiable achievements, action verbs, contact info, resume
  length, missing sections, and the specific skill gaps for this job)
- **Interview Question Generator** — technical questions for skills you have,
  "gap" questions for skills the job wants that you're missing, plus a mix of
  behavioral questions
- **PDF Report Export** — exports the full analysis (score, skills,
  suggestions, questions) as a PDF via a save dialog
- **Professional Dashboard** — tabbed layout (Dashboard / Suggestions /
  Interview Prep) instead of one long scrolling page

- **AI Career Coach** — sends the resume, job description, and analysis to
  Groq's API (Llama 3.3 70B) for personalized, specific coaching. Runs on a
  background thread so the UI doesn't freeze while waiting.

## Setting up the AI Career Coach

1. Copy `.env.example` to `.env`
2. Put your Groq API key in `.env`: `GROQ_API_KEY=your_key_here`
3. `.env` is already in `.gitignore` — it will never get committed

Get a key at https://console.groq.com/keys. If a key was ever pasted into a
chat, a doc, or committed to a repo, treat it as compromised and generate a
new one — don't keep using it.

## Structure

```
main.py                 - UI (CustomTkinter tabbed dashboard)
core/analyzer.py         - ATS score + skill matching
core/skills.py            - skill keyword list
core/suggestions.py      - dynamic resume suggestions
core/interview.py         - interview question generator
core/report.py            - PDF report export (reportlab)
```
