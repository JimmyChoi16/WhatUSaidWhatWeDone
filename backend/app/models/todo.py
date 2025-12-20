from datetime import datetime
from ..extensions import db


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default="Pending")
    author = db.Column(db.String(128), nullable=False)
    heat = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
