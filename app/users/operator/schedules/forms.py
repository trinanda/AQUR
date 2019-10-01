from wtforms import SelectField, SubmitField
from flask_babel import _, lazy_gettext as _l
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField, TimeField
from wtforms.validators import required, ValidationError, Email
from flask_wtf import FlaskForm

from app.models import Teacher, type_of_class, day_name_list, Student, course_status, gender, Course


def courses_list():
    return Course.query.all()


class ScheduleForm(FlaskForm):
    student_email = EmailField(_l('Student email'), validators=[required()])
    course_name = SelectField(_l('Course name'), validators=[required('It seems the student didn\' pay any course ')],
                              choices=[()])
    type_of_class = SelectField(_l('Type of class'), validators=[required()], choices=type_of_class)
    teacher_email = EmailField(_l('Teacher email'), validators=[required()])
    course_status = SelectField(_l('Course status'), validators=[required()], choices=course_status)
    submit = SubmitField()

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a student email.'))

    def validate_teacher_email(self, field):
        if Teacher.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a teacher email.'))


class ScheduleDayForm(ScheduleForm):
    schedule_day = SelectField(_l('Day'), validators=[required()], choices=day_name_list)
    start_at = TimeField(_l('Start at'), validators=[required()])
    end_at = TimeField(_l('End at'), validators=[required()])

    schedule_day_2 = SelectField(_l('Day 2'), choices=day_name_list)
    start_at_2 = TimeField(_l('Start at 2'))
    end_at_2 = TimeField(_l('End at 2'))


class CheckScheduleForm(ScheduleDayForm):
    course_name = SelectField(_l('Course name'), validators=[required('It seems the student didn\' pay any course ')],
                              choices=[()])
    type_of_class = SelectField(_l('Type of class'), validators=[required()], choices=type_of_class)
    gender = SelectField(_l('Gender'), choices=gender)
    submit = SubmitField()


class RequisitionScheduleForm(ScheduleDayForm):
    student_email = EmailField(_l('Student email'), validators=[required(), Email()])
    course_name = QuerySelectField(_l('Course name'),
                                   validators=[required('It seems the student didn\' pay any course ')],
                                   query_factory=courses_list)
    type_of_class = SelectField(_l('Type of class'), validators=[required()], choices=type_of_class)
    submit = SubmitField()

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a student email.'))
