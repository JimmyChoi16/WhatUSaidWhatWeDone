"""bind todos to user

Revision ID: 2c4b1e9a1d1a
Revises: 6f4b2c7f2d2a
Create Date: 2025-12-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2c4b1e9a1d1a"
down_revision = "6f4b2c7f2d2a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("todos", sa.Column("user_id", sa.BigInteger(), nullable=True))
    op.create_index("ix_todos_user_id", "todos", ["user_id"], unique=False)
    op.create_foreign_key("fk_todos_user_id", "todos", "user", ["user_id"], ["id"])


def downgrade():
    op.drop_constraint("fk_todos_user_id", "todos", type_="foreignkey")
    op.drop_index("ix_todos_user_id", table_name="todos")
    op.drop_column("todos", "user_id")
