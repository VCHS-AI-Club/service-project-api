"""update user schema

Revision ID: eadfd368123a
Revises: 3a73a2cf9e44
Create Date: 2022-10-07 23:35:30.444340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eadfd368123a'
down_revision = '3a73a2cf9e44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('children', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('setup_labor', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('audio_visual', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('teaching', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('food', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('environment', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'environment')
    op.drop_column('users', 'food')
    op.drop_column('users', 'teaching')
    op.drop_column('users', 'audio_visual')
    op.drop_column('users', 'setup_labor')
    op.drop_column('users', 'children')
    # ### end Alembic commands ###
