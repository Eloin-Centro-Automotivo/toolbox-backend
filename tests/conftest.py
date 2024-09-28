# conftest.py

import pytest
from app import create_app, db
from models import Mechanic, Tool, DefaultInventory, ConferenceRecord


@pytest.fixture
def app():
    # Configure the app for testing
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # In-memory database for testing
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        # Optionally, populate initial data
        populate_test_db()
        yield app
        db.session.remove()
        db.drop_all()


def populate_test_db():
    # Add test mechanics
    mechanics = [
        Mechanic(name='Test Mechanic 1'),
        Mechanic(name='Test Mechanic 2')
    ]
    db.session.add_all(mechanics)
    db.session.commit()

    # Add test tools
    tools = [
        Tool(name='Test Tool 1', category='Test Category'),
        Tool(name='Test Tool 2', category='Test Category')
    ]
    db.session.add_all(tools)
    db.session.commit()

    # Associate tools with mechanics
    for mechanic in mechanics:
        for tool in tools:
            inventory = DefaultInventory(mechanic_id=mechanic.id, tool_id=tool.id)
            db.session.add(inventory)
    db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()
