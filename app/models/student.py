from app.models import User

from app import db


class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    job = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'with_polymorphic': '*'
    }
