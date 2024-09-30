# database/populate_db.py
from models import db
from models.mechanic import Mechanic
from models.tool import Tool
from models.default_inventory import DefaultInventory

def populate_db():
    if Mechanic.query.first():
        return

    mechanics = [
        Mechanic(name='Douglas'),
        Mechanic(name='Renan')
    ]
    db.session.add_all(mechanics)
    db.session.commit()

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

        Tool(name='Chave Catraca Reversivel com Encaixe 1/2 Pol.',
             category='Catraca'),

        Tool(name='Alicate Universal', category='Alicate'),
        Tool(name='Alicate de Pressao com Mordente Reto 10 Pol.',
             category='Alicate'),
    ]
    db.session.add_all(tools)
    db.session.commit()

    for mechanic in mechanics:
        for tool in tools:
            inventory = DefaultInventory(mechanic_id=mechanic.id, tool_id=tool.id)
            db.session.add(inventory)
    db.session.commit()
