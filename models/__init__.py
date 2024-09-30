# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .mechanic import Mechanic
from .tool import Tool
from .default_inventory import DefaultInventory
from .conference_record import ConferenceRecord
