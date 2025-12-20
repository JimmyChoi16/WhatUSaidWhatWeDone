import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "app.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 前端开发服务器地址（按需改）
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
