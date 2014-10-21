"""empty message

Revision ID: 14eebce173c1
Revises: 51b80ee2617f
Create Date: 2014-04-10 13:37:40.834304

"""

# revision identifiers, used by Alembic.
revision = '14eebce173c1'
down_revision = '51b80ee2617f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('post_id', sa.Integer(), nullable=True))
    op.drop_column('categories', 'page_id')
    op.add_column('category', sa.Column('category_name', sa.String(length=20), nullable=True))
    op.create_unique_constraint(None, 'category', ['category_name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'category')
    op.drop_column('category', 'category_name')
    op.add_column('categories', sa.Column('page_id', sa.INTEGER(), nullable=True))
    op.drop_column('categories', 'post_id')
    ### end Alembic commands ###