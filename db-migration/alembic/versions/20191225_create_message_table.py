"""baseline

Revision ID: bc25b5f8939g
Revises:
Create Date: 2019-12-25

"""

# revision identifiers, used by Alembic.
revision = "bc25b5f8939g"
down_revision = "bc25b5f8939f"
branch_labels = None
depends_on = None

import sqlalchemy as sa

from alembic import op


def upgrade():
    op.create_table(
        "message",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("date_time", sa.DateTime(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("message")
