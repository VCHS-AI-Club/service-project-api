"""create opps table

Revision ID: ca8708828235
Revises: 31abdfcfb4d4
Create Date: 2022-08-24 21:16:19.456147

"""
from fastapi_utils.guid_type import GUID

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ca8708828235"
down_revision = "31abdfcfb4d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database."""
    op.create_table(
        "opps",
        sa.Column("id", GUID),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("desc", sa.String, nullable=False),
    )


def downgrade() -> None:
    """Downgrade database."""
    op.drop_table("opps")
