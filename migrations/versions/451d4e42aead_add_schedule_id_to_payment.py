"""add schedule_id to Payment

Revision ID: 451d4e42aead
Revises: 61a83e70a6b2
Create Date: 2019-10-20 16:33:13.336625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '451d4e42aead'
down_revision = '61a83e70a6b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('schedule_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'payment', 'schedule', ['schedule_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.drop_column('payment', 'schedule_id')
    # ### end Alembic commands ###