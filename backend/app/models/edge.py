import enum
import uuid
from datetime import datetime, timedelta
from ..extensions import db

def beijing_now():
    return datetime.utcnow() + timedelta(hours=8)

class EdgeStatus(enum.Enum):
    ACTIVE = "active"
    PAST = "past"
    BLOCKED = "blocked"


class Edge(db.Model):
    __tablename__ = "edges"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    from_node_id = db.Column(db.String(36), db.ForeignKey("nodes.id"), index=True, nullable=False)
    to_node_id = db.Column(db.String(36), db.ForeignKey("nodes.id"), index=True, nullable=False)
    edge_type_id = db.Column(db.String(36), db.ForeignKey("edge_types.id"), index=True)
    label = db.Column(db.String(255))
    strength = db.Column(db.SmallInteger)
    status = db.Column(db.Enum(EdgeStatus, name="edge_status_enum"))
    note = db.Column(db.Text)
    meta = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=beijing_now, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=beijing_now, onupdate=beijing_now, nullable=False
    )

    from_node = db.relationship("Node", foreign_keys=[from_node_id])
    to_node = db.relationship("Node", foreign_keys=[to_node_id])
    edge_type = db.relationship("EdgeType", backref="edges")
