"""
Reporlab

"""

import io
from typing import List

import reportlab
from finedu_portfolio.models import Company
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas, pdfimages
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)


def generate_portfolio_pdf(company: Company, metric_name: str, timeline: list,
                           financial_info: list, filename: str):
    """
    Generates a PDF report containing company, metric, timeline and financial information.

    Args:
        company: The company object.
        metric_name: The selected financial metric name.
        timeline: The list of financial data points for the metric.
        financial_info: The dictionary containing additional financial information.

    Returns:
        An in-memory binary buffer containing the generated PDF report.
    """

    buffer = io.BytesIO()

    fileName = f'{metric_name} - {company.ticker}.pdf'

    data: List = [['Fiscal Year', f'{metric_name}']]
    data.extend([(timeline[i], financial_info[i])
                for i in range(len(timeline))])

    pdf = SimpleDocTemplate(fileName, pagesize=letter)
    table = Table(data)
    elements = []

    # company_logo = ""
    # logo = PDFImage(company_logo, width=2*inch, height=0.8*inch)
    # elements.append(logo)

    header_text = f"{company.name} - {metric_name}"
    elements.append(Spacer(1*inch, 0.2*inch))  # Add some space after logo
    header_style = ParagraphStyle(
        name='HeaderStyle',
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=20
    )
    elements.append(Paragraph(header_text, style=header_style))

    elements.append(table)
    pdf.build(elements)

    return buffer
