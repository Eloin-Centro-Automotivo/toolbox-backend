# routes/__init__.py

from .conference_routes import conference_bp
from .mechanic_routes import mechanic_bp
from .report_routes import report_bp
from .tool_routes import tool_bp

all_blueprints = [mechanic_bp, tool_bp, conference_bp, report_bp]
