"""foreignkey payment on schedule

Revision ID: f313d14e0d39
Revises: 2a125e5ee346
Create Date: 2019-09-11 22:15:22.596734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f313d14e0d39'
down_revision = '2a125e5ee346'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('schedule', 'schedule_day',
               existing_type=postgresql.ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day'),
               type_=sa.Enum('Sunday', 'Monday', 'Tuesday', 'Wenesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day'),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('schedule', 'schedule_day',
               existing_type=sa.Enum('Sunday', 'Monday', 'Tuesday', 'Wenesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day'),
               type_=postgresql.ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day'),
               existing_nullable=True)
    # ### end Alembic commands ###