# routes/mechanic_routes.py

from flask import Blueprint, request, jsonify
from models import db, Tool, DefaultInventory
from models.mechanic import Mechanic
from utils.default_tools import get_default_tools  # Importar a função criada


mechanic_bp = Blueprint('mechanic_bp', __name__)

@mechanic_bp.route('/mechanics', methods=['GET'])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify([m.to_dict() for m in mechanics])


@mechanic_bp.route('/mechanics', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Name is required.'}), 400

    mechanic = Mechanic(name=name)
    db.session.add(mechanic)
    db.session.commit()

    return jsonify(mechanic.to_dict()), 201


@mechanic_bp.route('/mechanics/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    return jsonify(mechanic.to_dict())


@mechanic_bp.route('/mechanics/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    data = request.get_json()
    name = data.get('name')

    if name:
        mechanic.name = name
        db.session.commit()

    return jsonify(mechanic.to_dict())


@mechanic_bp.route('/mechanics/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Mechanic deleted successfully.'}), 200


@mechanic_bp.route('/mechanics/<int:mechanic_id>/assign-default-inventory', methods=['POST'])
def assign_default_inventory(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    try:
        # Obter todas as ferramentas padrão
        default_tools = get_default_tools()

        # Verificar se as ferramentas padrão já existem no banco de dados
        existing_tools = {tool.name: tool for tool in Tool.query.all()}
        tools_to_add = []

        for tool_data in default_tools:
            if tool_data['name'] not in existing_tools:
                tool = Tool(name=tool_data['name'], category=tool_data['category'])
                db.session.add(tool)
                tools_to_add.append(tool)
            else:
                tool = existing_tools[tool_data['name']]
            # Associar a ferramenta ao inventário do mecânico
            existing_inventory = DefaultInventory.query.filter_by(
                mechanic_id=mechanic_id, tool_id=tool.id).first()
            if not existing_inventory:
                inventory = DefaultInventory(mechanic_id=mechanic_id, tool_id=tool.id)
                db.session.add(inventory)

        db.session.commit()
        return jsonify({'message': 'Default inventory assigned successfully.'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@mechanic_bp.route('/mechanics/assign-default-inventory-to-all', methods=['POST'])
def assign_default_inventory_to_all():
    mechanics = Mechanic.query.all()

    try:
        # Obter todas as ferramentas padrão
        default_tools = get_default_tools()

        # Verificar se as ferramentas padrão já existem no banco de dados
        existing_tools = {tool.name: tool for tool in Tool.query.all()}
        tools_to_add = []

        for tool_data in default_tools:
            if tool_data['name'] not in existing_tools:
                tool = Tool(name=tool_data['name'], category=tool_data['category'])
                db.session.add(tool)
                tools_to_add.append(tool)
            else:
                tool = existing_tools[tool_data['name']]
            for mechanic in mechanics:
                # Associar a ferramenta ao inventário do mecânico
                existing_inventory = DefaultInventory.query.filter_by(
                    mechanic_id=mechanic.id, tool_id=tool.id).first()
                if not existing_inventory:
                    inventory = DefaultInventory(mechanic_id=mechanic.id, tool_id=tool.id)
                    db.session.add(inventory)

        db.session.commit()
        return jsonify({'message': 'Default inventory assigned to all mechanics successfully.'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@mechanic_bp.route('/mechanics/<int:mechanic_id>/tools', methods=['GET'])
def get_mechanic_tools(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    inventory_items = DefaultInventory.query.filter_by(mechanic_id=mechanic_id).all()
    tool_ids = [item.tool_id for item in inventory_items]
    tools = Tool.query.filter(Tool.id.in_(tool_ids)).all()
    return jsonify([tool.to_dict() for tool in tools])

