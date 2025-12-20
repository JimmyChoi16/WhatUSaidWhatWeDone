from .db import register_db_commands

def register_commands(app):
    register_db_commands(app)
