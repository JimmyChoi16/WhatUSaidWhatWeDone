import enum
import uuid
from datetime import datetime
from ..extensions import db


class NodeType(enum.Enum):  #给“节点（node）”一个语义类型，用来说明“这个节点代表的是什么东西
    PERSON = "person"
    ORG = "org"
    PLACE = "place"
    EVENT = "event"
    CUSTOM = "custom"


class Node(db.Model):
    __tablename__ = "nodes"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    graph_id = db.Column(db.String(36), db.ForeignKey("graphs.id"), index=True, nullable=False)
    node_type = db.Column(
        db.Enum(NodeType, name="node_type_enum"),
        nullable=False,
        default=NodeType.CUSTOM,
    )
    title = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255))
    summary = db.Column(db.String(255))
    data = db.Column(db.JSON) # 可扩展字段，存储节点的额外信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    graph = db.relationship("Graph", backref="nodes")
    layout = db.relationship("NodeLayout", backref="node", uselist=False, cascade="all, delete-orphan")
