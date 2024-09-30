# models/default_inventory.py

from . import db

class DefaultInventory(db.Model):
    __tablename__ = 'default_inventory'
    id = db.Column(db.Integer, primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
