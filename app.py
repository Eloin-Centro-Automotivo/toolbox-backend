# app.py
import os
from datetime import datetime, date
from io import BytesIO

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.pdfgen import canvas

from models import db, Mechanic, Tool, DefaultInventory, ConferenceRecord


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    else:
        app.config.update(test_config)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    @app.before_request
    def create_tables():
        if not os.path.exists('./instance/database.db'):
            db.create_all()
            # Populate the database with initial data
            populate_db()
        else:
            # Tables already exist, do nothing
            pass

    def populate_db():
        # Check if data already exists
        if Mechanic.query.first():
            return

        # Add mechanics
        mechanics = [
            Mechanic(name='Douglas'),
            Mechanic(name='Renan')
        ]
        db.session.add_all(mechanics)
        db.session.commit()

        # Add tools
        tools = [
            Tool(name='Chave Combinada 6mm', category='Combinada'),
            Tool(name='Chave Combinada 7mm', category='Combinada'),
            Tool(name='Chave Combinada 8mm', category='Combinada'),
            Tool(name='Chave Combinada 9mm', category='Combinada'),
            Tool(name='Chave Combinada 10mm', category='Combinada'),
            Tool(name='Chave Combinada 11mm', category='Combinada'),
            Tool(name='Chave Combinada 12mm', category='Combinada'),
            Tool(name='Chave Combinada 13mm', category='Combinada'),
            Tool(name='Chave Combinada 14mm', category='Combinada'),
            Tool(name='Chave Combinada 15mm', category='Combinada'),
            Tool(name='Chave Combinada 16mm', category='Combinada'),
            Tool(name='Chave Combinada 17mm', category='Combinada'),
            Tool(name='Chave Combinada 18mm', category='Combinada'),
            Tool(name='Chave Combinada 19mm', category='Combinada'),
            Tool(name='Chave Combinada 20mm', category='Combinada'),
            Tool(name='Chave Combinada 21mm', category='Combinada'),
            Tool(name='Chave Combinada 22mm', category='Combinada'),

            Tool(name='Chave L tipo Tork T10', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T15', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T20', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T25', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T27', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T30', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T40', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T45', category='L tipo Tork'),
            Tool(name='Chave L tipo Tork T50', category='L tipo Tork'),

            Tool(name='Soquete Curto 13mm', category='Soquete Curto'),
            Tool(name='Soquete Curto 15mm', category='Soquete Curto'),
            Tool(name='Soquete Curto 16mm', category='Soquete Curto'),
            Tool(name='Soquete Curto 17mm', category='Soquete Curto'),
            Tool(name='Soquete Curto 19mm', category='Soquete Curto'),
            Tool(name='Soquete Curto 21mm', category='Soquete Curto'),
            Tool(name='Soquete Curto 22mm', category='Soquete Curto'),
            Tool(name='Soquete Curto 23mm', category='Soquete Curto'),

            Tool(name='Chave Allen 1.5mm', category='Allen'),
            Tool(name='Chave Allen 2mm', category='Allen'),
            Tool(name='Chave Allen 2.5mm', category='Allen'),
            Tool(name='Chave Allen 3mm', category='Allen'),
            Tool(name='Chave Allen 4mm', category='Allen'),
            Tool(name='Chave Allen 5mm', category='Allen'),
            Tool(name='Chave Allen 6mm', category='Allen'),
            Tool(name='Chave Allen 8mm', category='Allen'),
            Tool(name='Chave Allen 10mm', category='Allen'),

            Tool(name='Chave Biela tipo L 10mm', category='Biela tipo L'),
            Tool(name='Chave Biela tipo L 11mm', category='Biela tipo L'),
            Tool(name='Chave Biela tipo L 13mm', category='Biela tipo L'),
            Tool(name='Chave Biela tipo L 17mm', category='Biela tipo L'),
            Tool(name='Chave Biela tipo L 19mm', category='Biela tipo L'),

            Tool(name='Martelo Bola com Cabo de Fibra 400g ', category='Martelo'),

            Tool(name='Chave de Fenda tam. Media', category='Fenda'),
            Tool(name='Chave de Fenda tam. Grande', category='Fenda'),

            Tool(name='Chave de Philips tam. Media', category='Philips'),
            Tool(name='Chave de Philips tam. Grande', category='Philips'),

            Tool(name='Chave Catraca Reversivel com Encaixe 1/2 Pol.', category='Catraca'),

            Tool(name='Alicate Universal', category='Alicate'),
            Tool(name='Alicate de Pressao com Mordente Reto 10 Pol.', category='Alicate'),
        ]
        db.session.add_all(tools)
        db.session.commit()

        # Associate all tools with all mechanics (default inventory)
        for mechanic in mechanics:
            for tool in tools:
                inventory = DefaultInventory(mechanic_id=mechanic.id, tool_id=tool.id)
                db.session.add(inventory)
        db.session.commit()

    @app.route('/mechanics', methods=['GET'])
    def get_mechanics():
        mechanics = Mechanic.query.all()
        return jsonify([m.to_dict() for m in mechanics])

    @app.route('/tools', methods=['GET'])
    def get_tools():
        tools = Tool.query.all()
        return jsonify([t.to_dict() for t in tools])

    @app.route('/conference', methods=['POST'])
    def post_conference():
        data = request.get_json()
        mechanic_id = data['mechanic_id']
        present_tools = data['present_tools']  # List of present tool IDs
        today = date.today()

        # Get all tools from the default inventory for the mechanic
        inventory = DefaultInventory.query.filter_by(mechanic_id=mechanic_id).all()
        all_tool_ids = [item.tool_id for item in inventory]

        # Calculate missing tools
        missing_tool_ids = list(set(all_tool_ids) - set(present_tools))

        # Remove existing records for the mechanic on today's date
        ConferenceRecord.query.filter_by(date=today, mechanic_id=mechanic_id).delete()

        # Add new records for missing tools
        for tool_id in missing_tool_ids:
            record = ConferenceRecord(
                date=today,
                mechanic_id=mechanic_id,
                tool_id=tool_id
            )
            db.session.add(record)
        db.session.commit()
        return jsonify({'message': 'Conferencia realizada com sucesso!'})

    @app.route('/reports/daily', methods=['GET'])
    def get_daily_report():
        date_str = request.args.get('date')  # Example format: 'YYYY-MM-DD'
        report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        buffer = generate_report(report_date)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='relatorio-diario.pdf', mimetype='application/pdf')


    def generate_report(report_date):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        y = 800

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, f"Relatorio de ferramentas ausentes - {report_date.strftime('%d/%m/%Y')}")
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
                p.drawString(50, y, f"Mecanico: {mechanic.name}")
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

    @app.route('/reports/missing_tools', methods=['GET'])
    def get_missing_tools_report():
        date_str = request.args.get('date')  # Exemplo: '2023-10-01'
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

    @app.route('/reports/missing_tools/pdf', methods=['GET'])
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

    # Create a new mechanic
    @app.route('/mechanics', methods=['POST'])
    def create_mechanic():
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Name is required.'}), 400
        mechanic = Mechanic(name=name)
        db.session.add(mechanic)
        db.session.commit()
        return jsonify(mechanic.to_dict()), 201

    # Get a specific mechanic
    @app.route('/mechanics/<int:mechanic_id>', methods=['GET'])
    def get_mechanic(mechanic_id):
        mechanic = Mechanic.query.get_or_404(mechanic_id)
        return jsonify(mechanic.to_dict())

    # Update a mechanic
    @app.route('/mechanics/<int:mechanic_id>', methods=['PUT'])
    def update_mechanic(mechanic_id):
        mechanic = Mechanic.query.get_or_404(mechanic_id)
        data = request.get_json()
        name = data.get('name')
        if name:
            mechanic.name = name
            db.session.commit()
        return jsonify(mechanic.to_dict())

    # Delete a mechanic
    @app.route('/mechanics/<int:mechanic_id>', methods=['DELETE'])
    def delete_mechanic(mechanic_id):
        mechanic = Mechanic.query.get_or_404(mechanic_id)
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify({'message': 'Mechanic deleted successfully.'}), 200

    # New CRUD Endpoints for Tool

    # Create a new tool
    @app.route('/tools', methods=['POST'])
    def create_tool():
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        if not name or not category:
            return jsonify({'error': 'Name and category are required.'}), 400
        tool = Tool(name=name, category=category)
        db.session.add(tool)
        db.session.commit()
        return jsonify(tool.to_dict()), 201

    # Get a specific tool
    @app.route('/tools/<int:tool_id>', methods=['GET'])
    def get_tool(tool_id):
        tool = Tool.query.get_or_404(tool_id)
        return jsonify(tool.to_dict())

    # Update a tool
    @app.route('/tools/<int:tool_id>', methods=['PUT'])
    def update_tool(tool_id):
        tool = Tool.query.get_or_404(tool_id)
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        if name:
            tool.name = name
        if category:
            tool.category = category
        db.session.commit()
        return jsonify(tool.to_dict())

    # Delete a tool
    @app.route('/tools/<int:tool_id>', methods=['DELETE'])
    def delete_tool(tool_id):
        tool = Tool.query.get_or_404(tool_id)
        db.session.delete(tool)
        db.session.commit()
        return jsonify({'message': 'Tool deleted successfully.'}), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
