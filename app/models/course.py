from sqlalchemy.dialects.postgresql import ARRAY

from app import db
from app.models.selectfield_helpers import TypeOfCourse

taught_courses = db.Table(
    'taught_courses',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('teacher.id')),
    db.Column('course_id', db.Integer(), db.ForeignKey('course.id')),
)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    image = db.Column(db.Unicode(128))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def course_name(self):
        return '%s' % (self.name)


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(ARRAY(db.Integer, db.ForeignKey('student.id')))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    type_of_course = db.Column(db.Enum(TypeOfCourse, name='type_of_course'))
    schedule = db.Column(db.DateTime())
    schedule_until = db.Column(db.DateTime())
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
