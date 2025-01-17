"""fixed_payment model

Revision ID: 03e55d601a6f
Revises: b2898a43a08b
Create Date: 2019-10-10 08:15:49.304176

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '03e55d601a6f'
down_revision = 'b2898a43a08b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fixed_payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('registration_payment', 'status_of_payment',
               existing_type=postgresql.ENUM('PENDING', 'INSTALLMENT', 'REJECTED', 'COMPLETED', 'EXPIRED', name='status_of_payment'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('registration_payment', 'status_of_payment',
               existing_type=postgresql.ENUM('PENDING', 'INSTALLMENT', 'REJECTED', 'COMPLETED', 'EXPIRED', name='status_of_payment'),
               nullable=False)
    op.drop_table('fixed_payment')
    # ### end Alembic commands ###
