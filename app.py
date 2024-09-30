# app.py
import os

from flask import Flask
from flask_cors import CORS

from models import db
from routes import all_blueprints


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    else:
        app.config.update(test_config)

    db.init_app(app)

    @app.before_request
    def setup():
        if not os.path.exists('./database.db'):
            db.create_all()
        else:
            pass

    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
