# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mecanico(db.Model):
    __tablename__ = 'mecanicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}

class Ferramenta(db.Model):
    __tablename__ = 'ferramentas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'categoria': self.categoria}

class InventarioPadrao(db.Model):
    __tablename__ = 'inventario_padrao'
    id = db.Column(db.Integer, primary_key=True)
    mecanico_id = db.Column(db.Integer, db.ForeignKey('mecanicos.id'), nullable=False)
    ferramenta_id = db.Column(db.Integer, db.ForeignKey('ferramentas.id'), nullable=False)

class RegistroConferencia(db.Model):
    __tablename__ = 'registros_conferencia'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    mecanico_id = db.Column(db.Integer, db.ForeignKey('mecanicos.id'), nullable=False)
    ferramenta_id = db.Column(db.Integer, db.ForeignKey('ferramentas.id'), nullable=False)
