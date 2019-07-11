import enum

from app import db


class PaymentStatus(enum.Enum):
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    total = db.Column(db.Integer)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    status = db.Column(db.Enum(PaymentStatus, name='payment_status'))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
