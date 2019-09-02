"""redefenition gender class

Revision ID: c02988795c6e
Revises: 7c8c6818ddc1
Create Date: 2019-09-02 14:16:13.864718

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c02988795c6e'
down_revision = '7c8c6818ddc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('course', 'name',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.alter_column('users', 'date_of_birth',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'date_of_birth',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('course', 'name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
    # ### end Alembic commands ###