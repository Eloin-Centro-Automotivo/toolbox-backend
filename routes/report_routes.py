# routes/report_routes.py
from collections import defaultdict
from datetime import datetime

from flask import Blueprint, request, jsonify, send_file

from models.conference_record import ConferenceRecord
from models.tool import Tool
from utils.pdf_utils import generate_report, generate_aggregate_report

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


@report_bp.route('/reports/missing-tools-aggregate', methods=['GET'])
def get_missing_tools_aggregate_report():
    date_str = request.args.get('date')  # Exemplo: 'YYYY-MM-DD'
    if not date_str:
        return jsonify({'error': 'Date parameter is required.'}), 400

    try:
        report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    try:
        # Obter todos os registros de ferramentas faltantes na data especificada
        missing_records = ConferenceRecord.query.filter_by(date=report_date).all()

        # Dicionário para contar as ferramentas faltantes
        missing_tools_count = defaultdict(int)

        for record in missing_records:
            missing_tools_count[record.tool_id] += 1

        # Converter os IDs das ferramentas para seus nomes e categorias
        aggregated_missing_tools = []
        for tool_id, count in missing_tools_count.items():
            tool = Tool.query.get(tool_id)
            if tool:
                aggregated_missing_tools.append({
                    'tool_id': tool.id,
                    'tool_name': tool.name,
                    # 'category': tool.category,
                    'count': count
                })

        # Ordenar o relatório por quantidade decrescente ou outro critério desejado
        aggregated_missing_tools = sorted(aggregated_missing_tools, key=lambda x: x['count'], reverse=True)

        buffer = generate_aggregate_report(report_date, aggregated_missing_tools)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='aggregated_missing_tools_report.pdf',
                         mimetype='application/pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 500