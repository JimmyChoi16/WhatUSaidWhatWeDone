from flask import Blueprint, request

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return {"error": "username/password required"}, 400

    # Demo：永远成功（你后面可以换 JWT / session / 查库）
    return {"message": "login ok", "user": username}
