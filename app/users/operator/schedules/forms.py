from flask_wtf import Form
from wtforms import SelectField, SubmitField
from wtforms.fields.html5 import EmailField, TimeField

from wtforms.validators import required, ValidationError

from app.models import Teacher, type_of_class, day_name_list, Student, course_status


class ScheduleForm(Form):
    student_email = EmailField('Student email', validators=[required()])
    course_name = SelectField('Course name', validators=[required('It seems the student didn\' pay any course ')],
                              choices=[()])
    type_of_class = SelectField('Type of class', validators=[required()], choices=type_of_class)
    schedule_day = SelectField('Day', choices=day_name_list)
    start_at = TimeField('Start at', validators=[required()])
    end_at = TimeField('End at', validators=[required()])
    teacher_email = EmailField('Teacher email', validators=[required()])
    course_status = SelectField('Course status', validators=[required()], choices=course_status)
    submit = SubmitField('OK')

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError('It seems the email not registered as a student.')

    def validate_teacher_email(self, field):
        if Teacher.query.filter_by(email=field.data).first() is None:
            raise ValidationError('It seems the email not registered as a teacher.')
