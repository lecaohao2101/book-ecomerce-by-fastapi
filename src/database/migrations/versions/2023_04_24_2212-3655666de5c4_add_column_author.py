"""add column author

Revision ID: 3655666de5c4
Revises: 4c02ae7a3725
Create Date: 2023-04-24 22:12:25.331132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3655666de5c4'
down_revision = '4c02ae7a3725'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('author', sa.Column('image', sa.String(), nullable=True))
    op.add_column('author', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('author', 'description')
    op.drop_column('author', 'image')
    # ### end Alembic commands ###