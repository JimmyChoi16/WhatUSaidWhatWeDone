import uuid
from datetime import datetime
from ..extensions import db


class EdgeType(db.Model):
    __tablename__ = "edge_types"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    directed = db.Column(db.Boolean, default=False, nullable=False)
    color = db.Column(db.String(32), nullable=False)
    style = db.Column(db.JSON, nullable=False)
    icon = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
