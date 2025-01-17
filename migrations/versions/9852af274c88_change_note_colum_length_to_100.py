"""change note colum length to 100

Revision ID: 9852af274c88
Revises: 2f581d6350fd
Create Date: 2019-11-04 07:44:00.378707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9852af274c88'
down_revision = '2f581d6350fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payment', 'note',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payment', 'note',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###
