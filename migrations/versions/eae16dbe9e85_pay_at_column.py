"""pay_at column

Revision ID: eae16dbe9e85
Revises: c176d37d52f0
Create Date: 2019-10-20 14:20:13.017002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eae16dbe9e85'
down_revision = 'c176d37d52f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('pay_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment', 'pay_at')
    # ### end Alembic commands ###
