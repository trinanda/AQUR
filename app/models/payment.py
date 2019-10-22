from app import db
from app.models import PaymentStatus, RegistrationPaymentStatus


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=True)
    total = db.Column(db.Integer)
    status_of_payment = db.Column(db.Enum(PaymentStatus, name='status_of_payment'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    student = db.relationship("Student", foreign_keys=[student_id])

    def __str__(self):
        return str(self.status_of_payment)


class RegistrationPayment(db.Model):
    __tablename__ = 'registration_payment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    total = db.Column(db.Integer)
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id'))
    status_of_payment = db.Column(db.Enum(RegistrationPaymentStatus, name='status_of_payment'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    course = db.relationship("Course", foreign_keys=[course_id])
    student = db.relationship("Student", foreign_keys=[student_id])

    def __str__(self):
        return str(self.status_of_payment)
