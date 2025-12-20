from flask import Blueprint, jsonify, request, abort
from sqlalchemy import desc
from ..extensions import db
from ..models import Todo

bp = Blueprint("todos", __name__, url_prefix="/api/todos")

VALID_STATUSES = {"Pending", "In Progress", "Completed"}


def serialize(todo: Todo):
    return {
        "id": todo.id,
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


@bp.post("")
def create_todo():
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    author = (data.get("author") or "").strip()
    status = (data.get("status") or "Pending").strip() or "Pending"

    if not title or not content or not author:
        abort(400, description="title, content, and author are required")
    if status not in VALID_STATUSES:
        abort(400, description=f"status must be one of {', '.join(VALID_STATUSES)}")

    todo = Todo(
        title=title,
        content=content,
        author=author,
        status=status,
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
def update_status(todo_id: int):
    data = request.get_json() or {}
    status = (data.get("status") or "").strip()
    if status and status not in VALID_STATUSES:
        abort(400, description=f"status must be one of {', '.join(VALID_STATUSES)}")

    todo = Todo.query.get(todo_id)
    if not todo:
        abort(404, description="Todo not found")

    if status:
        todo.status = status
    db.session.commit()
    return jsonify(serialize(todo))
