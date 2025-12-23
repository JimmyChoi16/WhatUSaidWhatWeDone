from datetime import datetime
from ..extensions import db


class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=False, index=True)
    token_hash = db.Column(db.String(64), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_agent = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))

    user = db.relationship("User", backref="refresh_tokens")
