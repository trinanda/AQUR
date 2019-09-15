from flask_wtf import Form
from wtforms import SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms_components import TimeField

from wtforms.validators import required, ValidationError

from app.models import Course, Teacher, type_of_class, day_name_list, month_name_list, Student


def course_list():
    return Course.query.all()


class ScheduleForm(Form):
    student_email = EmailField('Student email', validators=[required()])
    course_name = QuerySelectField('Course name', validators=[required()], query_factory=course_list)
    type_of_class = SelectField('Type of class', validators=[required()], choices=type_of_class)
    schedule_month = SelectField('Month', choices=month_name_list)
    schedule_day = SelectField('Day', choices=day_name_list)
    start_at = TimeField('Start at')
    end_at = TimeField('End at')
    teacher_email = EmailField('Teacher email', validators=[required()])
    submit = SubmitField('OK')

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError('It seems the email not registered as a student.')

    def validate_teacher_email(self, field):
        if Teacher.query.filter_by(email=field.data).first() is None:
            raise ValidationError('It seems the email not registered as a teacher.')
