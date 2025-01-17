"""remove fixed_payment and temporary_payment

Revision ID: c176d37d52f0
Revises: e57a2d730028
Create Date: 2019-10-20 14:07:05.911885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c176d37d52f0'
down_revision = 'e57a2d730028'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('temporary_payment')
    op.drop_table('fixed_payment')
    op.add_column('registration_payment', sa.Column('course_id', sa.Integer(), nullable=True))
    op.add_column('registration_payment', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('registration_payment', sa.Column('status_of_payment', sa.Enum('PENDING', 'INSTALLMENT', 'COMPLETED', name='status_of_payment'), nullable=True))
    op.add_column('registration_payment', sa.Column('student_id', sa.Integer(), nullable=True))
    op.add_column('registration_payment', sa.Column('total', sa.Integer(), nullable=True))
    op.add_column('registration_payment', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.drop_constraint('registration_payment_payment_id_fkey', 'registration_payment', type_='foreignkey')
    op.create_foreign_key(None, 'registration_payment', 'course', ['course_id'], ['id'])
    op.create_foreign_key(None, 'registration_payment', 'student', ['student_id'], ['id'])
    op.drop_column('registration_payment', 'payment_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registration_payment', sa.Column('payment_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'registration_payment', type_='foreignkey')
    op.drop_constraint(None, 'registration_payment', type_='foreignkey')
    op.create_foreign_key('registration_payment_payment_id_fkey', 'registration_payment', 'payment', ['payment_id'], ['id'])
    op.drop_column('registration_payment', 'updated_at')
    op.drop_column('registration_payment', 'total')
    op.drop_column('registration_payment', 'student_id')
    op.drop_column('registration_payment', 'status_of_payment')
    op.drop_column('registration_payment', 'created_at')
    op.drop_column('registration_payment', 'course_id')
    op.create_table('fixed_payment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('payment_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], name='fixed_payment_payment_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='fixed_payment_pkey')
    )
    op.create_table('temporary_payment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('payment_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], name='temporary_payment_payment_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='temporary_payment_pkey')
    )
    # ### end Alembic commands ###
