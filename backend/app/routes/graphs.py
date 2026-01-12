from flask import Blueprint, abort, current_app, jsonify, request
import jwt
from ..models import User
from ..service.graphs import (
    GraphServiceError,
    create_graph as create_graph_service,
    serialize_graph,
)

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


@bp.post("")
def create_graph():
    user = _require_user()
    data = request.get_json() or {}
    print(data)
    try:
        graph, created_nodes, created_edges = create_graph_service(user, data)
    except GraphServiceError as exc:
        abort(exc.status_code, description=exc.message)
    return jsonify(serialize_graph(graph, created_nodes, created_edges)), 201
