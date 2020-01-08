"""baseline

Revision ID: bc25b5f8939f
Revises:
Create Date: 2019-12-25

"""

# revision identifiers, used by Alembic.
revision = "bc25b5f8939f"
down_revision = None
branch_labels = None
depends_on = None

import sqlalchemy as sa

from alembic import op


def upgrade():
    op.create_table(
        "discord_user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_name", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("discord_user")
