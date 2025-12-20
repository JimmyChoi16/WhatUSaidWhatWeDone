from flask import Flask
from flask_cors import CORS

from config import Config
from app.extensions import db, migrate


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # CORS：开发阶段可放开；生产建议指定前端域名
    cors_origins = app.config.get("CORS_ORIGINS", "*")
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.errors import errors_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(errors_bp)  # 兜底错误处理

    return app
