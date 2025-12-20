import os
from sqlalchemy import text
from ..extensions import db

def register_db_commands(app):
    @app.cli.command("db_init")
    def db_init():
        db_name = os.getenv("DB_NAME")

        engine = db.create_engine(
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/?charset=utf8mb4"
        )

        with engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                    "DEFAULT CHARACTER SET utf8mb4 "
                    "DEFAULT COLLATE utf8mb4_unicode_ci;"
                )
            )
            conn.commit()

        from ..models import User, Todo  # noqa
        db.create_all()
        print(f"Database `{db_name}` initialized.")
