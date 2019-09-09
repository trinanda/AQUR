"""revision models

Revision ID: 90c40e4ba0ea
Revises: fce46e1de123
Create Date: 2019-09-08 17:16:07.646517

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '90c40e4ba0ea'
down_revision = 'fce46e1de123'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('course_id', sa.Integer(), nullable=True))

    payment_for_month = postgresql.ENUM('January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augustus', 'September', 'October', 'November', 'December', name='payment_for_month')
    payment_for_month.create(op.get_bind())
    op.add_column('payment', sa.Column('payment_for_month', sa.Enum('January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augustus', 'September', 'October', 'November', 'December', name='payment_for_month'), nullable=True))

    status_of_payment = postgresql.ENUM('PENDING', 'INSTALLMENT', 'REJECTED', 'COMPLETED', 'EXPIRED',name='status_of_payment')
    status_of_payment.create(op.get_bind())
    op.add_column('payment', sa.Column('status_of_payment', sa.Enum('PENDING', 'INSTALLMENT', 'REJECTED', 'COMPLETED', 'EXPIRED', name='status_of_payment'), nullable=True))

    type_of_class = postgresql.ENUM('REGULAR', 'PRIVATE', name='type_of_class')
    type_of_class.create(op.get_bind())
    op.add_column('payment', sa.Column('type_of_class', sa.Enum('REGULAR', 'PRIVATE', name='type_of_class'), nullable=True))

    op.drop_constraint('payment_name_key', 'payment', type_='unique')
    op.create_foreign_key(None, 'payment', 'course', ['course_id'], ['id'])
    op.drop_column('payment', 'status')
    op.drop_column('payment', 'name')
    op.add_column('schedule', sa.Column('duration', sa.Integer(), nullable=True))
    op.add_column('schedule', sa.Column('payment_id', postgresql.ARRAY(Integer(), as_tuple=ForeignKey('payment.id')), nullable=True))

    schedule_day = postgresql.ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day')
    schedule_day.create(op.get_bind())
    op.add_column('schedule', sa.Column('schedule_day', sa.Enum('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day'), nullable=True))

    schedule_month = postgresql.ENUM('January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augustus', 'September', 'October', 'November', 'December', name='schedule_month')
    schedule_month.create(op.get_bind())
    op.add_column('schedule', sa.Column('schedule_month', sa.Enum('January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augustus', 'September', 'October', 'November', 'December', name='schedule_month'), nullable=True))

    op.add_column('schedule', sa.Column('schedule_time', sa.Time(), nullable=True))
    op.drop_constraint('schedule_course_id_fkey', 'schedule', type_='foreignkey')
    op.drop_column('schedule', 'schedule')
    op.drop_column('schedule', 'type_of_course')
    op.drop_column('schedule', 'schedule_until')
    op.drop_column('schedule', 'course_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('schedule_until', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('type_of_course', postgresql.ENUM('REGULAR', 'PRIVATE', name='type_of_course'), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('schedule', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.create_foreign_key('schedule_course_id_fkey', 'schedule', 'course', ['course_id'], ['id'])
    op.drop_column('schedule', 'schedule_time')
    op.drop_column('schedule', 'schedule_month')
    op.drop_column('schedule', 'schedule_day')
    op.drop_column('schedule', 'payment_id')
    op.drop_column('schedule', 'duration')
    op.add_column('payment', sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('payment', sa.Column('status', postgresql.ENUM('PENDING', 'REJECTED', 'COMPLETED', name='payment_status'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.create_unique_constraint('payment_name_key', 'payment', ['name'])
    op.drop_column('payment', 'type_of_class')
    op.drop_column('payment', 'status_of_payment')
    op.drop_column('payment', 'payment_for_month')
    op.drop_column('payment', 'course_id')
    # ### end Alembic commands ###
