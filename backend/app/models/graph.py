import enum
import uuid
from datetime import datetime
from ..extensions import db


class Visibility(enum.Enum):
    PRIVATE = "private"
    SHARED = "shared"
    PUBLIC = "public"


class Graph(db.Model):
    __tablename__ = "graphs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), index=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    visibility = db.Column(
        db.Enum(Visibility, name="visibility_enum"),
        nullable=False,
        default=Visibility.PRIVATE,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    owner = db.relationship("User", backref="graphs")
