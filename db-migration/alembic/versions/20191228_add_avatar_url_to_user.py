"""baseline

Revision ID: bc25b5f8939g
Revises:
Create Date: 2019-12-28

"""

# revision identifiers, used by Alembic.
revision = "bc25b5f8939h"
down_revision = "bc25b5f8939g"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("discord_user", sa.Column("avatar_url", sa.String(), nullable=True))


def downgrade():
    op.drop_column("discord_user", "avatar_url")
