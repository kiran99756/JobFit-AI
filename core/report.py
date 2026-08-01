import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable


def generate_pdf_report(filepath, score, matched, missing, suggestions, questions):
    """Builds a JobFit AI analysis report as a PDF at the given filepath."""

    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "JobFitTitle", parent=styles["Title"], textColor=colors.HexColor("#1f6aa5")
    )
    heading_style = ParagraphStyle(
        "JobFitHeading", parent=styles["Heading3"], textColor=colors.HexColor("#1f6aa5"),
        spaceBefore=14, spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "JobFitBody", parent=styles["Normal"], spaceAfter=4, leading=15
    )
    score_style = ParagraphStyle(
        "JobFitScore", parent=styles["Heading1"], textColor=colors.HexColor("#2fa572")
    )

    story = []

    story.append(Paragraph("JobFit AI — Resume Analysis Report", title_style))
    story.append(Paragraph(
        datetime.datetime.now().strftime("Generated on %B %d, %Y at %I:%M %p"),
        styles["Normal"]
    ))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", color=colors.lightgrey))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"ATS Score: {score}%", score_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Matched Skills", heading_style))
    story.append(Paragraph(
        ", ".join(matched) if matched else "No direct matches found.", body_style
    ))

    story.append(Paragraph("Missing Skills", heading_style))
    story.append(Paragraph(
        ", ".join(missing) if missing else "No gaps — full skill coverage.", body_style
    ))

    story.append(Paragraph("Resume Suggestions", heading_style))
    for s in suggestions:
        story.append(Paragraph(f"&bull; {s}", body_style))

    story.append(Paragraph("Suggested Interview Questions", heading_style))
    for _, q, qtype in questions:
        story.append(Paragraph(f"<b>[{qtype.upper()}]</b> {q}", body_style))

    doc.build(story)
