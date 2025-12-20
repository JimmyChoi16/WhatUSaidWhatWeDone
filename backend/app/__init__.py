from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes import register_routes
from .commands import register_commands

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)
    register_commands(app)

    return app
