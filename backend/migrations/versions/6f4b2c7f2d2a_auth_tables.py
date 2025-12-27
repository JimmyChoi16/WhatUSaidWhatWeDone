"""auth tables

Revision ID: 6f4b2c7f2d2a
Revises: c1df6afbee18
Create Date: 2025-12-23 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6f4b2c7f2d2a"
down_revision = "c1df6afbee18"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("password_hash", sa.String(length=255), nullable=False, server_default=""),
    )
    op.add_column(
        "user",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
    )
    op.add_column(
        "user",
        sa.Column("failed_login_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )
    op.add_column("user", sa.Column("locked_until", sa.DateTime(), nullable=True))
    op.add_column("user", sa.Column("last_login_at", sa.DateTime(), nullable=True))
    op.add_column(
        "user",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"], unique=False)

    op.alter_column("user", "password_hash", server_default=None)
    op.alter_column("user", "is_active", server_default=None)
    op.alter_column("user", "failed_login_count", server_default=None)
    op.alter_column("user", "updated_at", server_default=None)


def downgrade():
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
    op.drop_column("user", "updated_at")
    op.drop_column("user", "last_login_at")
    op.drop_column("user", "locked_until")
    op.drop_column("user", "failed_login_count")
    op.drop_column("user", "is_active")
    op.drop_column("user", "password_hash")
