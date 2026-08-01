import random


SKILL_QUESTIONS = {
    "python": "Can you explain the difference between a list and a tuple in Python?",
    "java": "What is the difference between an interface and an abstract class in Java?",
    "javascript": "Explain how closures work in JavaScript.",
    "c++": "What's the difference between stack and heap memory allocation?",
    "c": "Explain how pointers work in C and a case where you used them.",
    "html": "What is semantic HTML, and why does it matter for accessibility and SEO?",
    "css": "Walk me through the CSS box model.",
    "sql": "What's the difference between an INNER JOIN and a LEFT JOIN?",
    "mysql": "How would you go about optimizing a slow MySQL query?",
    "mongodb": "When would you choose MongoDB over a relational database?",
    "react": "Explain the difference between state and props in React.",
    "node": "What is the event loop in Node.js, and why does it matter?",
    "django": "Describe Django's MVT (Model-View-Template) architecture.",
    "flask": "How does routing work in a Flask application?",
    "git": "What's the difference between `git merge` and `git rebase`?",
    "github": "Walk me through your workflow for contributing via a GitHub pull request.",
    "docker": "What's the difference between a Docker image and a container?",
    "kubernetes": "What role does a Pod play in Kubernetes?",
    "aws": "Which AWS services have you used, and what did you use them for?",
    "azure": "Which Azure services have you used, and what did you use them for?",
    "linux": "How would you find and terminate a running process from the Linux command line?",
    "excel": "What Excel functions or features do you rely on most for data analysis?",
    "power bi": "How have you used Power BI to build a dashboard or report?",
    "machine learning": "What's the difference between supervised and unsupervised learning?",
    "ai": "Describe a project where you applied an AI/ML concept in practice.",
}

GENERIC_QUESTIONS = [
    "Tell me about a challenging project you worked on and how you handled it.",
    "How do you stay current with new tools and technologies in your field?",
    "Describe a time you had to debug a particularly difficult issue.",
    "How do you prioritize when you're juggling multiple tasks or deadlines?",
    "Why are you interested in this specific role?",
    "Tell me about a time you disagreed with a teammate — how did you resolve it?",
    "What's a project you're proud of, and what was your specific contribution?",
]


def generate_questions(matched, missing, num_generic=3):
    """Returns a list of (skill, question, category) tuples.
    category is 'technical' (from matched skills), 'gap' (from missing
    skills, framed so the candidate can prep even without direct experience),
    or 'behavioral' (generic)."""

    questions = []

    for skill in matched:
        if skill in SKILL_QUESTIONS:
            questions.append((skill, SKILL_QUESTIONS[skill], "technical"))

    for skill in missing[:3]:
        if skill in SKILL_QUESTIONS:
            q = (
                f"This role expects {skill} — even without hands-on experience, "
                f"be ready to speak to it: {SKILL_QUESTIONS[skill]}"
            )
            questions.append((skill, q, "gap"))

    sample_size = min(num_generic, len(GENERIC_QUESTIONS))
    for q in random.sample(GENERIC_QUESTIONS, sample_size):
        questions.append(("General", q, "behavioral"))

    return questions
