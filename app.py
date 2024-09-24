# app.py
from datetime import datetime, date
from io import BytesIO

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.pdfgen import canvas

from models import db, Mecanico, Ferramenta, InventarioPadrao, \
    RegistroConferencia

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()
    # Popula o banco de dados com dados iniciais
    populate_db()


def populate_db():
    # Verifica se já existem dados
    if Mecanico.query.first():
        return

    # Adiciona mecânicos
    mecanicos = [
        Mecanico(nome='João'),
        Mecanico(nome='Maria'),
        Mecanico(nome='Carlos')
    ]
    db.session.add_all(mecanicos)
    db.session.commit()

    # Adiciona ferramentas
    ferramentas = [
        Ferramenta(nome='Chave Combinada 8mm', categoria='Chaves Combinadas'),
        Ferramenta(nome='Chave Combinada 9mm', categoria='Chaves Combinadas'),
        Ferramenta(nome='Chave Combinada 10mm', categoria='Chaves Combinadas'),
        Ferramenta(nome='Chave L 15mm', categoria='Chaves L'),
        Ferramenta(nome='Pito Grande 3mm', categoria='Pitos Grandes'),
        # Adicione todas as ferramentas necessárias...
    ]
    db.session.add_all(ferramentas)
    db.session.commit()

    # Associa todas as ferramentas a todos os mecânicos (inventário padrão)
    for mecanico in mecanicos:
        for ferramenta in ferramentas:
            inventario = InventarioPadrao(mecanico_id=mecanico.id, ferramenta_id=ferramenta.id)
            db.session.add(inventario)
    db.session.commit()


@app.route('/mecanicos', methods=['GET'])
def get_mecanicos():
    mecanicos = Mecanico.query.all()
    return jsonify([m.to_dict() for m in mecanicos])


@app.route('/ferramentas', methods=['GET'])
def get_ferramentas():
    ferramentas = Ferramenta.query.all()
    return jsonify([f.to_dict() for f in ferramentas])


@app.route('/conferencia', methods=['POST'])
def post_conferencia():
    data = request.get_json()
    mecanico_id = data['mecanico_id']
    ferramentas_faltantes = data['ferramentas_faltantes']  # Lista de IDs de ferramentas faltantes
    hoje = date.today()

    # Remove registros existentes para o mecânico na data de hoje
    RegistroConferencia.query.filter_by(data=hoje, mecanico_id=mecanico_id).delete()

    # Adiciona novos registros
    for ferramenta_id in ferramentas_faltantes:
        registro = RegistroConferencia(
            data=hoje,
            mecanico_id=mecanico_id,
            ferramenta_id=ferramenta_id
        )
        db.session.add(registro)
    db.session.commit()
    return jsonify({'message': 'Conferência registrada com sucesso!'})


@app.route('/relatorios/diario', methods=['GET'])
def get_relatorio_diario():
    data_str = request.args.get('data')  # Exemplo de formato: 'YYYY-MM-DD'
    data_relatorio = datetime.strptime(data_str, '%Y-%m-%d').date()
    buffer = gerar_relatorio(data_relatorio)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='relatorio_diario.pdf', mimetype='application/pdf')


def gerar_relatorio(data_relatorio):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Relatório de Ferramentas Faltantes - {data_relatorio.strftime('%d/%m/%Y')}")
    y -= 40

    registros = RegistroConferencia.query.filter_by(data=data_relatorio).all()

    if not registros:
        p.setFont("Helvetica", 12)
        p.drawString(50, y, "Nenhuma ferramenta faltante registrada.")
    else:
        mecanicos_ids = list(set([r.mecanico_id for r in registros]))
        for mecanico_id in mecanicos_ids:
            mecanico = Mecanico.query.get(mecanico_id)
            p.setFont("Helvetica-Bold", 14)
            p.drawString(50, y, f"Mecânico: {mecanico.nome}")
            y -= 20
            registros_mecanico = [r for r in registros if r.mecanico_id == mecanico_id]
            p.setFont("Helvetica", 12)
            for registro in registros_mecanico:
                ferramenta = Ferramenta.query.get(registro.ferramenta_id)
                p.drawString(70, y, f"- {ferramenta.nome} ({ferramenta.categoria})")
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
