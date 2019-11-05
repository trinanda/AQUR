from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import SelectField, SubmitField, TextAreaField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import required, ValidationError

from app.models import Course, payment_status, Student, registration_payment_status
from wtforms.fields.html5 import EmailField, IntegerField


class ManipulatePaymentForm(FlaskForm):
    student_email_or_phone_number = StringField(_l('Student email or phone number'), validators=[required()])
    total = IntegerField(_l('Total'), validators=[required()])
    status_of_payment = SelectField(_l('Payment Status'), choices=payment_status)
    note = TextAreaField(_l('Note'))
    submit = SubmitField()

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a student email.'))


class AddRegistrationPaymentForm(FlaskForm):
    student_email_or_phone_number = StringField(_l('Student email or phone number'), validators=[required()])
    total = IntegerField(_l('Total'), validators=[required()])
    course_name = QuerySelectField(_l('Course name'), validators=[required()], query_factory=lambda: Course.query.all())
    status_of_payment = SelectField(_l('Payment Status'), choices=registration_payment_status)
    submit = SubmitField()

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a student email.'))


def edit_registration_payment_form_factory(default_course_name):
    class EditRegistrationPaymentForm(AddRegistrationPaymentForm):
        course_name = QuerySelectField('Course name', query_factory=lambda: Course.query.all(),
                                       default=Course.query.filter_by(name=default_course_name).one())

    return EditRegistrationPaymentForm
