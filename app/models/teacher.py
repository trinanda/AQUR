from app.models import User
from app.models.course import taught_courses
from .. import db


class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    taught_courses = db.relationship('Course', secondary=taught_courses,
                                     backref=db.backref('teacher', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
        'with_polymorphic': '*'
    }
