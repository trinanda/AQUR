from app import db
from app.models.selectfield_properties import DayNameList, TypeOfClass


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    course_start_at = db.Column(db.Date())
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    time_schedule = db.relationship('TimeSchedule', backref='schedule', lazy=True)
    student = db.relationship("Student", foreign_keys=[student_id])
    teacher = db.relationship("Teacher", foreign_keys=[teacher_id])
    course = db.relationship("Course", foreign_keys=[course_id])
    payment = db.relationship("Payment", foreign_keys=[payment_id])


class TimeSchedule(db.Model):
    __tablename__ = 'time_schedule'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Enum(DayNameList, name='day'))
    start_at = db.Column(db.Time())
    end_at = db.Column(db.Time())
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=True)
    requisition_schedule_id = db.Column(db.Integer, db.ForeignKey('requisition_schedule.id'), nullable=True)


class RequisitionSchedule(db.Model):
    __tablename__ = 'requisition_schedule'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    type_of_class = db.Column(db.Enum(TypeOfClass, name='type_of_class'))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    time_schedule = db.relationship('TimeSchedule', backref='requisition_schedule', lazy=True)
    student = db.relationship("Student", foreign_keys=[student_id])
    course = db.relationship("Course", foreign_keys=[course_id])
