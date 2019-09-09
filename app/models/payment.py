from app import db
from app.models import MonthNameList, TypeOfClass, PaymentStatus


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    total = db.Column(db.Integer)
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id'))
    type_of_class = db.Column(db.Enum(TypeOfClass, name='type_of_class'))
    payment_for_month = db.Column(db.Enum(MonthNameList, name='payment_for_month'))
    status_of_payment = db.Column(db.Enum(PaymentStatus, name='status_of_payment'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
