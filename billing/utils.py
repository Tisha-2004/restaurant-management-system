"""PDF helpers built on ReportLab (invoices and reports)."""
from io import BytesIO

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ORANGE = colors.HexColor("#FC8019")


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Brand", fontSize=20, textColor=ORANGE, spaceAfter=4, leading=24))
    styles.add(ParagraphStyle(name="Muted", fontSize=9, textColor=colors.HexColor("#666666")))
    return styles


def _table_style():
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), ORANGE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E5E5E5")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFAFA")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )


def build_pdf(title, header_lines, table_data, filename, footer=""):
    """Render a branded PDF document and return it as an HTTP download response."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm)
    styles = _styles()
    story = [Paragraph(title, styles["Brand"])]
    for line in header_lines:
        story.append(Paragraph(line, styles["Muted"]))
    story.append(Spacer(1, 10 * mm))
    table = Table(table_data, hAlign="LEFT", repeatRows=1)
    table.setStyle(_table_style())
    story.append(table)
    if footer:
        story.append(Spacer(1, 8 * mm))
        story.append(Paragraph(footer, styles["Muted"]))
    doc.build(story)
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
