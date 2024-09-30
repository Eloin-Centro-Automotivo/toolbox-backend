# routes/conference_routes.py

from datetime import date

from flask import Blueprint, request, jsonify

from models import db
from models.conference_record import ConferenceRecord
from models.default_inventory import DefaultInventory

conference_bp = Blueprint('conference_bp', __name__)

@conference_bp.route('/conference', methods=['POST'])
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
    return jsonify({'message': 'Conferência realizada com sucesso!'})
