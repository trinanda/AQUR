from app.models import User

from app import db


class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    job = db.Column(db.String)
    description = db.Column(db.String(100))

    def __str__(self):
        return self.email

    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'with_polymorphic': '*',
        'inherit_condition': user_id == User.id
    }
