# utils/pdf_utils.py

from io import BytesIO
from reportlab.pdfgen import canvas
from models.mechanic import Mechanic
from models.tool import Tool
from models.conference_record import ConferenceRecord

def generate_report(report_date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Relatório de ferramentas ausentes - {report_date.strftime('%d/%m/%Y')}")
    y -= 40

    records = ConferenceRecord.query.filter_by(date=report_date).all()

    if not records:
        p.setFont("Helvetica", 12)
        p.drawString(50, y, "Nenhuma ferramenta ausente registrada.")
    else:
        mechanic_ids = list(set([r.mechanic_id for r in records]))
        for mechanic_id in mechanic_ids:
            mechanic = Mechanic.query.get(mechanic_id)
            p.setFont("Helvetica-Bold", 14)
            p.drawString(50, y, f"Mecânico: {mechanic.name}")
            y -= 20
            mechanic_records = [r for r in records if r.mechanic_id == mechanic_id]
            p.setFont("Helvetica", 12)
            for record in mechanic_records:
                tool = Tool.query.get(record.tool_id)
                p.drawString(70, y, f"- {tool.name} ({tool.category})")
                y -= 20
                if y < 50:
                    p.showPage()
                    y = 800
            y -= 10

    p.save()
    buffer.seek(0)
    return buffer

def generate_missing_tools_pdf(report_date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Relatório de Ferramentas Faltantes - {report_date.strftime('%d/%m/%Y')}")
    y -= 40

    missing_records = ConferenceRecord.query.filter_by(date=report_date).all()
    missing_tool_ids = {record.tool_id for record in missing_records}
    missing_tools = Tool.query.filter(Tool.id.in_(missing_tool_ids)).all()

    if not missing_tools:
        p.setFont("Helvetica", 12)
        p.drawString(50, y, "Nenhuma ferramenta faltante registrada.")
    else:
        p.setFont("Helvetica", 12)
        for tool in missing_tools:
            p.drawString(50, y, f"- {tool.name} ({tool.category})")
            y -= 20
            if y < 50:
                p.showPage()
                y = 800

    p.save()
    buffer.seek(0)
    return buffer
