# utils/pdf_utils.py

from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, \
    Spacer

from models import Tool, ConferenceRecord, Mechanic


def generate_report(report_date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Relatório de Ferramentas Ausentes - {report_date.strftime('%d/%m/%Y')}")
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


def generate_aggregate_report(report_date, aggregated_missing_tools):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50  # Posição inicial no eixo Y

    # Título do Relatório
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Relatório Agregado de Ferramentas Ausentes - {report_date.strftime('%d/%m/%Y')}")
    y -= 40

    if not aggregated_missing_tools:
        p.setFont("Helvetica", 12)
        p.drawString(50, y, "Nenhuma ferramenta ausente registrada para a data selecionada.")
    else:
        # Cabeçalhos da Tabela
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Ferramenta")
        p.drawString(400, y, "Quantidade")
        y -= 20
        p.line(50, y, width - 50, y)  # Linha horizontal abaixo dos cabeçalhos
        y -= 20

        # Conteúdo da Tabela
        p.setFont("Helvetica", 12)
        for tool in aggregated_missing_tools:
            if y < 50:
                p.showPage()
                y = height - 50
                # Repetir os cabeçalhos na nova página
                p.setFont("Helvetica-Bold", 12)
                p.drawString(50, y, "Nome da Ferramenta")
                p.drawString(400, y, "Quantidade Necessária")
                y -= 20
                p.line(50, y, width - 50, y)
                y -= 20
                p.setFont("Helvetica", 12)
            p.drawString(50, y, tool['tool_name'])
            p.drawString(400, y, str(tool['count']))
            y -= 20

    p.save()
    buffer.seek(0)
    return buffer


def generate_inventory_checklist_by_mechanic_pdf(categories, mechanic_names):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    elements = []

    # Título da Checklist
    title = Paragraph("Checklist do Inventário Padrão por Mecânico",
                      styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Data da Geração
    date_paragraph = Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y')}",
                               styles['Normal'])
    elements.append(date_paragraph)
    elements.append(Spacer(1, 24))

    # Cabeçalhos
    headers = ["Categoria", "Ferramenta"] + mechanic_names

    # Estilo da Tabela
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])

    data = [headers]

    # Conteúdo da Tabela
    for category, tools in categories.items():
        for idx, tool in enumerate(tools):
            if idx == 0:
                row = [category, tool.name] + [" " for _ in mechanic_names]
            else:
                row = ["", tool.name] + [" " for _ in mechanic_names]
            data.append(row)

    # Ajustar largura das colunas
    colWidths = [80, 225] + [70 for _ in mechanic_names]

    # Criar a tabela
    table = Table(data, colWidths=colWidths)
    table.setStyle(estilo)

    elements.append(table)

    # Construir o documento
    doc.build(elements)

    buffer.seek(0)
    return buffer