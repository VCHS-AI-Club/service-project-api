"""add user table

Revision ID: 135fd849c5e6
Revises: 137dcb265736
Create Date: 2022-08-31 00:35:31.743724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135fd849c5e6'
down_revision = '137dcb265736'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
