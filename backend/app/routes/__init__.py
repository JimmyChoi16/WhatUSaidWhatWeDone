from .health import bp as health_bp
from .todos import bp as todos_bp

def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(todos_bp)
