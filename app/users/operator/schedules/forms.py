from wtforms import SelectField, SubmitField, FieldList, FormField, StringField, TextAreaField
from flask_babel import _, lazy_gettext as _l
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import TimeField, DateField, IntegerField
from wtforms.validators import required, ValidationError, DataRequired
from flask_wtf import FlaskForm
from wtforms.widgets.html5 import NumberInput

from app.models import Teacher, type_of_class, day_name_list, Student, gender, Course, requisition_schedule_status


class TimeScheduleForm(FlaskForm):
    day = SelectField(_l('Day'), validators=[required()], choices=day_name_list)
    start_at = TimeField(_l('Start at'), validators=[required()])
    end_at = TimeField(_l('End at'), validators=[required()])


class ScheduleForm(FlaskForm):
    student_email_or_phone_number = StringField(_l('Student email or phone number'), validators=[required()])
    course_name = SelectField(_l('Course name'), validators=[required('It seems the student didn\' pay any course ')],
                              choices=[()])
    type_of_class = SelectField(_l('Type of class'), validators=[required()], choices=type_of_class)
    teacher_email_or_phone_number = StringField(_l('Teacher email or phone number'), validators=[required()])
    course_start_at = DateField(_l('Course Start at'), validators=[DataRequired()], format='%Y-%m-%d')
    how_many_times_in_a_week = IntegerField(widget=NumberInput(min=1, max=7))
    time_schedule = FieldList(FormField(TimeScheduleForm))
    submit = SubmitField()

    def validate_teacher_email(self, field):
        if Teacher.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a teacher email.'))


class CheckScheduleForm(TimeScheduleForm):
    course_name = SelectField(_l('Course name'), validators=[required('It seems the student didn\' pay any course ')],
                              choices=[()])
    type_of_class = SelectField(_l('Type of class'), validators=[required()], choices=type_of_class)
    gender = SelectField(_l('Gender'), choices=gender)
    submit = SubmitField()


class RequisitionScheduleForm(TimeScheduleForm):
    student_email_or_phone_number = StringField(_l('Student email or phone number'), validators=[required()])
    course_name = QuerySelectField(_l('Course name'),
                                   validators=[required('It seems the student didn\' pay any course ')],
                                   query_factory=lambda: Course.query.all())
    type_of_class = SelectField(_l('Type of class'), validators=[required()], choices=type_of_class)
    how_many_times_in_a_week = IntegerField(widget=NumberInput(min=1, max=7))
    requisition_schedule_status = SelectField(_l('Requisition Schedule Status'), validators=[required()],
                                              choices=requisition_schedule_status)
    time_schedule = FieldList(FormField(TimeScheduleForm))
    note = TextAreaField(_l('Note'))
    submit = SubmitField()

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a student email.'))


def edit_requisition_schedule_form_factory(default_requisition_status):
    class EditRequisitionScheduleForm(TimeScheduleForm):
        how_many_times_in_a_week = IntegerField(widget=NumberInput(min=1, max=7))
        requisition_schedule_status = SelectField(_l('Requisition Schedule Status'), validators=[required()],
                                                  choices=requisition_schedule_status,
                                                  default=default_requisition_status)
        note = TextAreaField(_l('Note'))
        time_schedule = FieldList(FormField(TimeScheduleForm))
        submit = SubmitField()

    return EditRequisitionScheduleForm
