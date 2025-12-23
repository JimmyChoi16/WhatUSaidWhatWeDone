import jwt
from flask import Blueprint, jsonify, request, abort, current_app
from sqlalchemy import desc
from ..extensions import db
from ..models import Todo, User

bp = Blueprint("todos", __name__, url_prefix="/api/todos")

VALID_STATUSES = {"Pending", "In Progress", "Completed"}


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


def serialize(todo: Todo):
    return {
        "id": todo.id,
        "user_id": todo.user_id,
        "title": todo.title,
        "content": todo.content,
        "status": todo.status,
        "author": todo.author,
        "heat": todo.heat,
        "created_at": todo.created_at.isoformat(),
        "updated_at": todo.updated_at.isoformat(),
    }


@bp.get("")
def list_todos():
    limit = request.args.get("limit", type=int)
    query = Todo.query.order_by(desc(Todo.created_at))
    if limit:
        query = query.limit(limit)
    todos = query.all()
    return jsonify([serialize(t) for t in todos])


@bp.get("/mine")
def list_my_todos():
    user = _require_user()
    todos = (
        Todo.query.filter_by(user_id=user.id)
        .order_by(desc(Todo.created_at))
        .all()
    )
    return jsonify([serialize(t) for t in todos])


@bp.post("")
def create_todo():
    user = _require_user()
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    status = (data.get("status") or "Pending").strip() or "Pending"

    if not title or not content:
        abort(400, description="title and content are required")
    if status not in VALID_STATUSES:
        abort(400, description=f"status must be one of {', '.join(VALID_STATUSES)}")

    todo = Todo(
        title=title,
        content=content,
        author=user.nickname or user.email,
        status=status,
        user_id=user.id,
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(serialize(todo)), 201


@bp.post("/<int:todo_id>/vote")
def vote(todo_id: int):
    data = request.get_json() or {}
    delta = data.get("delta", 1)
    try:
        delta = int(delta)
    except (TypeError, ValueError):
        abort(400, description="delta must be an integer")
    if delta not in (-1, 1):
        abort(400, description="delta must be -1 or 1")

    todo = Todo.query.get(todo_id)
    if not todo:
        abort(404, description="Todo not found")

    todo.heat = max(0, todo.heat + delta)
    db.session.commit()
    return jsonify(serialize(todo))


@bp.patch("/<int:todo_id>")
def update_todo(todo_id: int):
    user = _require_user()
    data = request.get_json() or {}
    title = data.get("title")
    content = data.get("content")
    status = (data.get("status") or "").strip() if "status" in data else ""
    if status and status not in VALID_STATUSES:
        abort(400, description=f"status must be one of {', '.join(VALID_STATUSES)}")

    todo = Todo.query.get(todo_id)
    if not todo:
        abort(404, description="Todo not found")
    if todo.user_id != user.id:
        abort(403, description="not allowed to update this todo")

    if title is not None:
        title = str(title).strip()
        if not title:
            abort(400, description="title cannot be empty")
        todo.title = title
    if content is not None:
        content = str(content).strip()
        if not content:
            abort(400, description="content cannot be empty")
        todo.content = content
    if status:
        todo.status = status
    db.session.commit()
    return jsonify(serialize(todo))


@bp.delete("/<int:todo_id>")
def delete_todo(todo_id: int):
    user = _require_user()
    todo = Todo.query.get(todo_id)
    if not todo:
        abort(404, description="Todo not found")
    if todo.user_id != user.id:
        abort(403, description="not allowed to delete this todo")

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"ok": True})
