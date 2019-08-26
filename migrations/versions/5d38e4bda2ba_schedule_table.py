"""schedule table

Revision ID: 5d38e4bda2ba
Revises: adeda21fbff7
Create Date: 2019-08-25 22:24:52.241762

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5d38e4bda2ba'
down_revision = 'adeda21fbff7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', postgresql.ARRAY(sa.Integer(), as_tuple=sa.ForeignKey('student.id')), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('type_of_course', postgresql.ENUM('REGULAR', 'PRIVATE', name='type_of_course', create_type=False), nullable=False),
    sa.Column('schedule', sa.DateTime(), nullable=True),
    sa.Column('schedule_until', sa.DateTime(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taught_courses',
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], )
    )
    op.create_unique_constraint(None, 'course', ['name'])
    op.drop_constraint('course_teacher_id_fkey', 'course', type_='foreignkey')
    op.drop_constraint('course_student_id_fkey', 'course', type_='foreignkey')
    op.drop_column('course', 'teacher_id')
    op.drop_column('course', 'type_of_course')
    op.drop_column('course', 'student_id')
    op.drop_column('course', 'schedule')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('schedule', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('course', sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('course', sa.Column('type_of_course', postgresql.ENUM('REGULAR', 'PRIVATE', name='type_of_course'), autoincrement=False, nullable=True))
    op.add_column('course', sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('course_student_id_fkey', 'course', 'student', ['student_id'], ['id'])
    op.create_foreign_key('course_teacher_id_fkey', 'course', 'teacher', ['teacher_id'], ['id'])
    op.drop_constraint(None, 'course', type_='unique')
    op.drop_table('taught_courses')
    op.drop_table('schedule')
    # ### end Alembic commands ###
