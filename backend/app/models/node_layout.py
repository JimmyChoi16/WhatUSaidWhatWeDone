from datetime import datetime
from ..extensions import db


class NodeLayout(db.Model):
    __tablename__ = "node_layouts"

    node_id = db.Column(db.String(36), db.ForeignKey("nodes.id"), primary_key=True)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    pinned = db.Column(db.Boolean, default=False, nullable=False)
    z_index = db.Column(db.Integer, default=0, nullable=False)
    style = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
