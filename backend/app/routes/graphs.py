from flask import Blueprint, abort, current_app, jsonify, request
import jwt
from ..extensions import db
from ..models import Graph, Node, NodeLayout, Edge, User
from ..models.graph import Visibility
from ..models.node import NodeType

bp = Blueprint("graphs", __name__, url_prefix="/api/graphs")


def _get_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ", 1)[1].strip()


def _decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        current_app.config["JWT_SECRET"],
        algorithms=[current_app.config["JWT_ALGORITHM"]],
    )


def _require_user() -> User:
    token = _get_bearer_token()
    if not token:
        abort(401, description="authorization required")
    try:
        payload = _decode_token(token)
    except jwt.ExpiredSignatureError:
        abort(401, description="access token expired")
    except jwt.InvalidTokenError:
        abort(401, description="invalid access token")

    if payload.get("type") != "access":
        abort(401, description="invalid token type")

    user = User.query.get(int(payload.get("sub", 0)))
    if not user or not user.is_active:
        abort(403, description="account not available")
    return user


def _parse_visibility(raw_value: str) -> Visibility:
    value = (raw_value or "private").strip().lower()
    for item in Visibility:
        if item.value == value:
            return item
    abort(400, description="visibility must be private, shared, or public")


def _parse_node_type(raw_value: str) -> NodeType:
    value = (raw_value or "custom").strip().lower()
    for item in NodeType:
        if item.value == value:
            return item
    abort(400, description="node_type must be person, org, place, event, or custom")


def _serialize_graph(graph: Graph, nodes: list[Node], edges: list[Edge]):
    return {
        "graph": {
            "id": graph.id,
            "name": graph.name,
            "visibility": graph.visibility.value,
            "owner_user_id": graph.owner_user_id,
            "created_at": graph.created_at.isoformat(),
            "updated_at": graph.updated_at.isoformat(),
        },
        "nodes": [
            {
                "id": node.id,
                "title": node.title,
                "node_type": node.node_type.value,
                "graph_id": node.graph_id,
            }
            for node in nodes
        ],
        "edges": [
            {
                "id": edge.id,
                "source": edge.from_node_id,
                "target": edge.to_node_id,
                "label": edge.label,
                "type": (edge.meta or {}).get("type"),
            }
            for edge in edges
        ],
    }


@bp.post("")
def create_graph():
    user = _require_user()
    data = request.get_json() or {}
    print(data)
    graph_data = data.get("graph") or {}
    graph_name = (graph_data.get("name") or "").strip()
    if not graph_name:
        abort(400, description="graph name is required")

    graph = Graph(
        owner_user_id=user.id,
        name=graph_name,
        description=graph_data.get("description"),
        visibility=_parse_visibility(graph_data.get("visibility")),
    )
    db.session.add(graph)

    nodes_payload = data.get("nodes") or []
    edges_payload = data.get("edges") or []
    if not isinstance(nodes_payload, list) or not isinstance(edges_payload, list):
        abort(400, description="nodes and edges must be lists")

    created_nodes: list[Node] = []
    created_edges: list[Edge] = []
    node_ids: set[str] = set()

    for node_payload in nodes_payload:
        if not isinstance(node_payload, dict):
            abort(400, description="each node must be an object")
        title = (node_payload.get("title") or "").strip()
        if not title:
            abort(400, description="node title is required")

        node_id = node_payload.get("id") or None
        node = Node(
            id=str(node_id) if node_id else None,
            graph_id=graph.id,
            node_type=_parse_node_type(node_payload.get("node_type")),
            title=title,
            avatar_url=node_payload.get("avatar_url"),
            summary=node_payload.get("summary"),
            data=node_payload.get("data") or {},
        )
        db.session.add(node)
        db.session.flush()
        node_ids.add(node.id)
        created_nodes.append(node)

        position = node_payload.get("position") or {}
        x = position.get("x")
        y = position.get("y")
        if x is None or y is None:
            abort(400, description="node position requires x and y")

        style = node_payload.get("style") or {}
        layout_style = dict(style) if isinstance(style, dict) else {}
        width = layout_style.pop("width", None)
        height = layout_style.pop("height", None)

        layout = NodeLayout(
            node_id=node.id,
            x=float(x),
            y=float(y),
            width=float(width) if width is not None else None,
            height=float(height) if height is not None else None,
            style=layout_style or None,
        )
        db.session.add(layout)

    for edge_payload in edges_payload:
        if not isinstance(edge_payload, dict):
            abort(400, description="each edge must be an object")
        source = edge_payload.get("source")
        target = edge_payload.get("target")
        if not source or not target:
            abort(400, description="edge source and target are required")
        if source not in node_ids or target not in node_ids:
            abort(400, description="edge endpoints must reference known nodes")

        edge_id = edge_payload.get("id") or None
        edge = Edge(
            id=str(edge_id) if edge_id else None,
            from_node_id=source,
            to_node_id=target,
            label=edge_payload.get("label"),
            meta={
                "type": edge_payload.get("type"),
                "style": edge_payload.get("style"),
            },
        )
        db.session.add(edge)
        created_edges.append(edge)

    db.session.commit()
    return jsonify(_serialize_graph(graph, created_nodes, created_edges)), 201
