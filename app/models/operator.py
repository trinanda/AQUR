from app.models import User

from app import db


class Operator(User):
    __tablename__ = 'operator'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'operator',
        'with_polymorphic': '*'
    }
