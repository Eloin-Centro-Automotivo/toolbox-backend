# routes/report_routes.py

from datetime import datetime

from flask import Blueprint, request, jsonify, send_file
from utils.pdf_utils import generate_report, generate_missing_tools_pdf

from models.conference_record import ConferenceRecord
from models.tool import Tool

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/reports/daily', methods=['GET'])
def get_daily_report():
    date_str = request.args.get('date')  # Example format: 'YYYY-MM-DD'
    if not date_str:
        return jsonify({'error': 'Date parameter is required.'}), 400

    try:
        report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    buffer = generate_report(report_date)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='relatorio-diario.pdf', mimetype='application/pdf')

@report_bp.route('/reports/missing_tools', methods=['GET'])
def get_missing_tools_report():
    date_str = request.args.get('date')  # Exemplo: 'YYYY-MM-DD'
    if not date_str:
        return jsonify({'error': 'Date parameter is required.'}), 400

    try:
        report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Obter todos os registros de ferramentas faltantes na data especificada
    missing_records = ConferenceRecord.query.filter_by(date=report_date).all()

    # Obter IDs únicos das ferramentas faltantes
    missing_tool_ids = {record.tool_id for record in missing_records}

    # Obter detalhes das ferramentas faltantes
    missing_tools = Tool.query.filter(Tool.id.in_(missing_tool_ids)).all()

    # Converter as ferramentas para dicionários
    missing_tools_data = [tool.to_dict() for tool in missing_tools]

    return jsonify(missing_tools_data)

@report_bp.route('/reports/missing_tools/pdf', methods=['GET'])
def get_missing_tools_report_pdf():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date parameter is required.'}), 400

    try:
        report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    buffer = generate_missing_tools_pdf(report_date)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='relatorio-ferramentas-faltantes.pdf',
        mimetype='application/pdf'
    )
