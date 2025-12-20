from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from .routes import register_routes
from .commands import register_commands

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow frontend (default localhost:3000) to call APIs. Adjust origins via env if needed.
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # Avoid redirecting between /api/todos and /api/todos/ on preflight
    app.url_map.strict_slashes = False

    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)
    register_commands(app)

    return app
