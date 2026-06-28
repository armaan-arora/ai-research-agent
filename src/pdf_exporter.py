from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import HexColor
import re
import io

def generate_pdf(topic, report, evaluation=None):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )

    styles = getSampleStyleSheet()
    
    # custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        textColor=HexColor("#1a1a2e"),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=HexColor("#16213e"),
        spaceAfter=10,
        spaceBefore=15
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceAfter=8
    )

    score_style = ParagraphStyle(
        "ScoreStyle",
        parent=styles["Normal"],
        fontSize=12,
        textColor=HexColor("#0f3460"),
        spaceAfter=6
    )

    elements = []

    # title
    elements.append(Paragraph(f"Research Report: {topic}", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # evaluation scores if available
    if evaluation:
        elements.append(Paragraph("Report Quality Scores", heading_style))
        elements.append(Paragraph(f"Coverage:  {evaluation.get('coverage')}/10", score_style))
        elements.append(Paragraph(f"Citations: {evaluation.get('citations')}/10", score_style))
        elements.append(Paragraph(f"Clarity:   {evaluation.get('clarity')}/10", score_style))
        elements.append(Paragraph(f"Depth:     {evaluation.get('depth')}/10", score_style))
        elements.append(Paragraph(f"Overall:   {evaluation.get('overall')}/10", score_style))
        elements.append(Paragraph(f"Feedback: {evaluation.get('feedback')}", body_style))
        elements.append(Spacer(1, 0.3 * inch))

    # report content — parse markdown
    lines = report.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            elements.append(Spacer(1, 0.1 * inch))
        elif line.startswith("## "):
            elements.append(Paragraph(line.replace("## ", ""), heading_style))
        elif line.startswith("### "):
            elements.append(Paragraph(line.replace("### ", ""), heading_style))
        elif line.startswith("# "):
            elements.append(Paragraph(line.replace("# ", ""), title_style))
        elif line.startswith("- ") or line.startswith("* "):
            elements.append(Paragraph(f"• {line[2:]}", body_style))
        else:
            # clean markdown bold/italic
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
            elements.append(Paragraph(line, body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer