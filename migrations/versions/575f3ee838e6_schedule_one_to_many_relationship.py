"""schedule one-to-many relationship

Revision ID: 575f3ee838e6
Revises: 5881e8ab3988
Create Date: 2019-09-23 07:30:44.656121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '575f3ee838e6'
down_revision = '5881e8ab3988'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scheduleday',
    sa.Column('id', sa.Integer(), nullable=False),


    sa.Column('day', sa.Enum('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', name='day'), nullable=True),

    sa.Column('start_at', sa.Time(), nullable=True),
    sa.Column('end_at', sa.Time(), nullable=True),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('schedule', 'start_at_2')
    op.drop_column('schedule', 'schedule_day')
    op.drop_column('schedule', 'end_at')
    op.drop_column('schedule', 'schedule_day_2')
    op.drop_column('schedule', 'end_at_2')
    op.drop_column('schedule', 'start_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('start_at', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('end_at_2', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('schedule_day_2', postgresql.ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day_2'), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('end_at', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('schedule_day', postgresql.ENUM('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', name='schedule_day'), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('start_at_2', postgresql.TIME(), autoincrement=False, nullable=True))
    op.drop_table('scheduleday')
    # ### end Alembic commands ###