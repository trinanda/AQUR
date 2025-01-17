"""add how many times in a week to requistion schedule

Revision ID: 7d27b5b2dc87
Revises: e003fc33d314
Create Date: 2019-10-26 10:40:57.770827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d27b5b2dc87'
down_revision = 'e003fc33d314'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requisition_schedule', sa.Column('how_many_times_in_a_week', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('requisition_schedule', 'how_many_times_in_a_week')
    # ### end Alembic commands ###
