"""empty message

Revision ID: 3ea38cb13b40
Revises: 6836a69f78f
Create Date: 2014-04-08 20:39:19.438158

"""

# revision identifiers, used by Alembic.
revision = '3ea38cb13b40'
down_revision = '6836a69f78f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('poet', sa.String(length=80), nullable=True))
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.drop_column('user', 'password')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=40), nullable=True))
    op.drop_column('user', 'password_hash')
    op.drop_column('post', 'poet')
    ### end Alembic commands ###
