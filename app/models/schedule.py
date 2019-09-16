from sqlalchemy.orm import relationship

from app import db
from app.models.selectfield_properties import DayNameList, TypeOfClass, CourseStatus


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    type_of_class = db.Column(db.Enum(TypeOfClass, name='type_of_class'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    schedule_day = db.Column(db.Enum(DayNameList, name='schedule_day'))
    start_at = db.Column(db.Time())
    end_at = db.Column(db.Time())
    course_status = db.Column(db.Enum(CourseStatus, name='course_status'))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    student = relationship("Student", foreign_keys=[student_id])
    teacher = relationship("Teacher", foreign_keys=[teacher_id])
    course = relationship("Course", foreign_keys=[course_id])
    payment = relationship("Payment", foreign_keys=[payment_id])
