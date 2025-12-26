import hashlib
import time
import uuid
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import RefreshToken, User

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _now() -> datetime:
    return datetime.utcnow()


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _encode_token(user_id: int, token_type: str, expires_in: timedelta) -> str:
    now_ts = int(time.time())
    exp_ts = now_ts + int(expires_in.total_seconds())
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "jti": uuid.uuid4().hex,
        "iat": now_ts,
        "exp": exp_ts,
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm=current_app.config["JWT_ALGORITHM"])


def _decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        current_app.config["JWT_SECRET"],
        algorithms=[current_app.config["JWT_ALGORITHM"]],
    )


def _issue_tokens(user: User, req):
    access_ttl = timedelta(minutes=current_app.config["JWT_ACCESS_TTL_MINUTES"])
    refresh_ttl = timedelta(days=current_app.config["JWT_REFRESH_TTL_DAYS"])
    access_token = _encode_token(user.id, "access", access_ttl)
    refresh_token = _encode_token(user.id, "refresh", refresh_ttl)

    token_hash = _hash_token(refresh_token)
    refresh_entry = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=_now() + refresh_ttl,
        user_agent=req.headers.get("User-Agent"),
        ip_address=req.remote_addr,
    )
    db.session.add(refresh_entry)
    db.session.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int(access_ttl.total_seconds()),
    }


def _serialize_user(user: User):
    return {
        "id": user.id,
        "email": user.email,
        "nickname": user.nickname,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
    }


def _get_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ", 1)[1].strip()


def _require_access_user():
    token = _get_bearer_token()
    if not token:
        return None, ("authorization required", 401)
    try:
        payload = _decode_token(token)
    except jwt.ExpiredSignatureError:
        return None, ("access token expired", 401)
    except jwt.InvalidTokenError:
        return None, ("invalid access token", 401)
    if payload.get("type") != "access":
        return None, ("invalid token type", 401)

    user = User.query.get(int(payload.get("sub", 0)))
    if not user or not user.is_active:
        return None, ("account not available", 403)
    return user, None


@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    nickname = (data.get("nickname") or "").strip()

    if not email or not password or not nickname:
        return jsonify({"error": "email, password, and nickname are required"}), 400
    if "@" not in email or "." not in email:
        return jsonify({"error": "email is invalid"}), 400
    if len(password) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400

    user = User(email=email, nickname=nickname)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "email already registered"}), 409

    tokens = _issue_tokens(user, request)
    return jsonify({"user": _serialize_user(user), **tokens}), 201


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and not user.is_active:
        return jsonify({"error": "account is disabled"}), 403
    if user and user.is_locked():
        return jsonify({"error": "too many failed attempts, try later"}), 429

    if not user or not user.check_password(password):
        if user:
            user.failed_login_count += 1
            max_attempts = current_app.config["AUTH_MAX_FAILED_ATTEMPTS"]
            if user.failed_login_count >= max_attempts:
                lock_minutes = current_app.config["AUTH_LOCKOUT_MINUTES"]
                user.locked_until = _now() + timedelta(minutes=lock_minutes)
            db.session.commit()
        return jsonify({"error": "invalid credentials"}), 401

    user.failed_login_count = 0
    user.locked_until = None
    user.last_login_at = _now()
    db.session.commit()

    tokens = _issue_tokens(user, request)
    return jsonify({"user": _serialize_user(user), **tokens})


@bp.post("/refresh")
def refresh():
    data = request.get_json(silent=True) or {}
    refresh_token = (data.get("refresh_token") or "").strip()
    if not refresh_token:
        return jsonify({"error": "refresh_token is required"}), 400

    try:
        payload = _decode_token(refresh_token)
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "refresh token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid refresh token"}), 401

    if payload.get("type") != "refresh":
        return jsonify({"error": "invalid token type"}), 401

    token_hash = _hash_token(refresh_token)
    token_entry = RefreshToken.query.filter_by(token_hash=token_hash).first()
    if not token_entry or token_entry.revoked_at:
        return jsonify({"error": "refresh token revoked"}), 401
    if token_entry.expires_at <= _now():
        return jsonify({"error": "refresh token expired"}), 401

    user = User.query.get(int(payload.get("sub", 0)))
    if not user or not user.is_active:
        return jsonify({"error": "account not available"}), 403

    token_entry.revoked_at = _now()
    db.session.commit()

    tokens = _issue_tokens(user, request)
    return jsonify({"user": _serialize_user(user), **tokens})


@bp.post("/logout")
def logout():
    data = request.get_json(silent=True) or {}
    refresh_token = (data.get("refresh_token") or "").strip()
    if not refresh_token:
        return jsonify({"error": "refresh_token is required"}), 400

    token_hash = _hash_token(refresh_token)
    token_entry = RefreshToken.query.filter_by(token_hash=token_hash).first()
    if token_entry and not token_entry.revoked_at:
        token_entry.revoked_at = _now()
        db.session.commit()

    return jsonify({"ok": True})


@bp.get("/me")
def me():
    user, error = _require_access_user()
    if error:
        message, code = error
        return jsonify({"error": message}), code
    return jsonify({"user": _serialize_user(user)})


@bp.post("/password")
def change_password():
    user, error = _require_access_user()
    if error:
        message, code = error
        return jsonify({"error": message}), code

    data = request.get_json(silent=True) or {}
    current_password = data.get("current_password") or ""
    new_password = data.get("new_password") or ""

    if not current_password or not new_password:
        return jsonify({"error": "current_password and new_password are required"}), 400
    if not user.check_password(current_password):
        return jsonify({"error": "current password is incorrect"}), 401
    if len(new_password) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"ok": True})
