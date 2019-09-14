"""make some revision on schedule model

Revision ID: 56dd9be84ea6
Revises: 90c40e4ba0ea
Create Date: 2019-09-11 11:34:29.451294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56dd9be84ea6'
down_revision = '90c40e4ba0ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('course_id', sa.Integer(), nullable=True))
    op.add_column('schedule', sa.Column('type_of_class', sa.Enum('REGULAR', 'PRIVATE', name='type_of_class'), nullable=True))
    op.create_foreign_key(None, 'schedule', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_column('schedule', 'type_of_class')
    op.drop_column('schedule', 'course_id')
    # ### end Alembic commands ###