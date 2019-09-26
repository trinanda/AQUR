from wtforms import SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField, TimeField
from wtforms.validators import required, ValidationError

from flask_wtf import Form
from wtforms.validators import Email

from app.models import Teacher, type_of_class, day_name_list, Student, course_status, gender, Course


def courses_list():
    return Course.query.all()


class ScheduleForm(Form):
    student_email = EmailField('Student email', validators=[required()])
    course_name = SelectField('Course name', validators=[required('It seems the student didn\' pay any course ')],
                              choices=[()])
    type_of_class = SelectField('Type of class', validators=[required()], choices=type_of_class)
    teacher_email = EmailField('Teacher email', validators=[required()])
    course_status = SelectField('Course status', validators=[required()], choices=course_status)
    submit = SubmitField('OK')

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError('It seems the email is not registered as a student email.')

    def validate_teacher_email(self, field):
        if Teacher.query.filter_by(email=field.data).first() is None:
            raise ValidationError('It seems the email is not registered as a teacher email.')


class CheckScheduleForm(Form):
    course_name = SelectField('Course name', validators=[required('It seems the student didn\' pay any course ')],
                              choices=[()])
    type_of_class = SelectField('Type of class', validators=[required()], choices=type_of_class)
    schedule_day = SelectField('Day', choices=day_name_list)
    start_at = TimeField('Start at', validators=[required()])
    end_at = TimeField('End at', validators=[required()])
    gender = SelectField('Gender', choices=gender)
    submit = SubmitField('OK')


class ScheduleDayForm(ScheduleForm):
    schedule_day = SelectField('Day', validators=[required()], choices=day_name_list)
    start_at = TimeField('Start at', validators=[required()])
    end_at = TimeField('End at', validators=[required()])

    schedule_day_2 = SelectField('Day 2', choices=day_name_list)
    start_at_2 = TimeField('Start at 2')
    end_at_2 = TimeField('End at 2 ')


class RequisitionScheduleForm(ScheduleDayForm):
    student_email = EmailField('Student email', validators=[required(), Email()])
    course_name = QuerySelectField('Course name', validators=[required('It seems the student didn\' pay any course ')],
                                   query_factory=courses_list)
    type_of_class = SelectField('Type of class', validators=[required()], choices=type_of_class)
    submit = SubmitField()

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError('It seems the email is not registered as a student email.')
