# routes/mechanic_routes.py

from flask import Blueprint, request, jsonify
from models import db
from models.mechanic import Mechanic

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
