# app.py
from datetime import datetime, date
from io import BytesIO
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.pdfgen import canvas

from models import db, Mechanic, Tool, DefaultInventory, ConferenceRecord

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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
        Tool(name='8mm Combination Wrench', category='Combination Wrenches'),
        Tool(name='9mm Combination Wrench', category='Combination Wrenches'),
        Tool(name='10mm Combination Wrench', category='Combination Wrenches'),

        Tool(name='15mm L Wrench', category='L Wrenches'),

        Tool(name='Large 3mm Punch', category='Large Punches'),
        # Add all necessary tools...
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
    return jsonify({'message': 'Conference successfully recorded!'})


@app.route('/reports/daily', methods=['GET'])
def get_daily_report():
    date_str = request.args.get('date')  # Example format: 'YYYY-MM-DD'
    report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    buffer = generate_report(report_date)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='daily_report.pdf', mimetype='application/pdf')


def generate_report(report_date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Missing Tools Report - {report_date.strftime('%d/%m/%Y')}")
    y -= 40

    records = ConferenceRecord.query.filter_by(date=report_date).all()

    if not records:
        p.setFont("Helvetica", 12)
        p.drawString(50, y, "No missing tools recorded.")
    else:
        mechanic_ids = list(set([r.mechanic_id for r in records]))
        for mechanic_id in mechanic_ids:
            mechanic = Mechanic.query.get(mechanic_id)
            p.setFont("Helvetica-Bold", 14)
            p.drawString(50, y, f"Mechanic: {mechanic.name}")
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


if __name__ == '__main__':
    app.run(debug=True)
