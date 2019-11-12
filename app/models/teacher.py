from app.models import User
from .. import db


class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    taught_course = db.relationship('TaughtCourse', backref='teacher', lazy='dynamic')
    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
        'with_polymorphic': '*',
        'inherit_condition': user_id == User.id
    }


class TaughtCourse(db.Model):
    __tablename__ = 'taught_course'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref='taught_course', lazy=True)
