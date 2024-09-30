# routes/tool_routes.py

from flask import Blueprint, request, jsonify
from models import db
from models.tool import Tool

tool_bp = Blueprint('tool_bp', __name__)

@tool_bp.route('/tools', methods=['GET'])
def get_tools():
    tools = Tool.query.all()
    return jsonify([t.to_dict() for t in tools])

@tool_bp.route('/tools', methods=['POST'])
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

@tool_bp.route('/tools/<int:tool_id>', methods=['GET'])
def get_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    return jsonify(tool.to_dict())

@tool_bp.route('/tools/<int:tool_id>', methods=['PUT'])
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

@tool_bp.route('/tools/<int:tool_id>', methods=['DELETE'])
def delete_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    db.session.delete(tool)
    db.session.commit()
    return jsonify({'message': 'Tool deleted successfully.'}), 200
