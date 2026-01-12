from __future__ import annotations

from ..extensions import db
from ..models import Edge, Graph, Node, NodeLayout, User
from ..models.graph import Visibility
from ..models.node import NodeType


class GraphServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def parse_visibility(raw_value: str) -> Visibility:
    value = (raw_value or "private").strip().lower()
    for item in Visibility:
        if item.value == value:
            return item
    raise GraphServiceError("visibility must be private, shared, or public")


def parse_node_type(raw_value: str) -> NodeType:
    value = (raw_value or "custom").strip().lower()
    for item in NodeType:
        if item.value == value:
            return item
    raise GraphServiceError("node_type must be person, org, place, event, or custom")


def serialize_graph(graph: Graph, nodes: list[Node], edges: list[Edge]) -> dict:
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


def create_graph(user: User, data: dict) -> tuple[Graph, list[Node], list[Edge]]:
    graph_data = data.get("graph") or {}
    graph_name = (graph_data.get("name") or "").strip()
    if not graph_name:
        raise GraphServiceError("graph name is required")

    graph = Graph(
        owner_user_id=user.id,
        name=graph_name,
        description=graph_data.get("description"),
        visibility=parse_visibility(graph_data.get("visibility")),
    )
    db.session.add(graph)
    db.session.flush()

    nodes_payload = data.get("nodes") or []
    edges_payload = data.get("edges") or []
    if not isinstance(nodes_payload, list) or not isinstance(edges_payload, list):
        raise GraphServiceError("nodes and edges must be lists")

    created_nodes: list[Node] = []
    created_edges: list[Edge] = []
    node_ids: set[str] = set()
    client_id_map: dict[str, str] = {}

    for node_payload in nodes_payload:
        if not isinstance(node_payload, dict):
            raise GraphServiceError("each node must be an object")
        title = (node_payload.get("title") or "").strip()
        if not title:
            raise GraphServiceError("node title is required")

        client_node_id = node_payload.get("id")
        if client_node_id is not None:
            client_node_id = str(client_node_id)
            if client_node_id in client_id_map:
                raise GraphServiceError(
                    f"node id '{client_node_id}' is duplicated in payload", status_code=409
                )
        node = Node(
            id=None,
            graph_id=graph.id,
            node_type=parse_node_type(node_payload.get("node_type")),
            title=title,
            avatar_url=node_payload.get("avatar_url"),
            summary=node_payload.get("summary"),
            data=node_payload.get("data") or {},
        )
        db.session.add(node)
        db.session.flush()
        node_ids.add(node.id)
        if client_node_id is not None:
            client_id_map[client_node_id] = node.id
        created_nodes.append(node)

        position = node_payload.get("position") or {}
        x = position.get("x")
        y = position.get("y")
        if x is None or y is None:
            raise GraphServiceError("node position requires x and y")

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
            raise GraphServiceError("each edge must be an object")
        source = edge_payload.get("source")
        target = edge_payload.get("target")
        if not source or not target:
            raise GraphServiceError("edge source and target are required")
        source_id = client_id_map.get(str(source)) if client_id_map else None
        target_id = client_id_map.get(str(target)) if client_id_map else None
        if source_id is None or target_id is None:
            raise GraphServiceError("edge endpoints must reference known nodes")

        edge = Edge(
            from_node_id=source_id,
            to_node_id=target_id,
            label=edge_payload.get("label"),
            meta={
                "type": edge_payload.get("type"),
                "style": edge_payload.get("style"),
            },
        )
        db.session.add(edge)
        created_edges.append(edge)

    db.session.commit()
    return graph, created_nodes, created_edges
