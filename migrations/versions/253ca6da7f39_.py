"""empty message

Revision ID: 253ca6da7f39
Revises: 4a38af23530f
Create Date: 2016-04-08 13:27:09.013314

"""

# revision identifiers, used by Alembic.
revision = '253ca6da7f39'
down_revision = '4a38af23530f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###