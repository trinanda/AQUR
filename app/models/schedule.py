from sqlalchemy.dialects.postgresql import ARRAY

from app import db
from app.models.selectfield_properties import DayNameList, MonthNameList


# TODO | search able teacher and student name using jquery tags input autocomplete

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(ARRAY(db.Integer, db.ForeignKey('payment.id')))

    student_id = db.Column(ARRAY(db.Integer, db.ForeignKey('student.id')))

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    schedule_month = db.Column(db.Enum(MonthNameList, name='schedule_month'))
    schedule_day = db.Column(db.Enum(DayNameList, name='schedule_day'))
    schedule_time = db.Column(db.Time())
    duration = db.Column(db.Integer())

    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
