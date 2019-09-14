from app.models import User
from app.models.course import taught_courses
from .. import db


class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    taught_courses = db.relationship('Course', secondary=taught_courses, lazy='subquery',
                                     backref=db.backref('courses', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
        'with_polymorphic': '*',
        'inherit_condition': user_id == User.id
    }
