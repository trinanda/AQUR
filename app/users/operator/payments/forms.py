from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import required, ValidationError

from app.models import Course, type_of_class, month_name_list, payment_status, Student


def course_list():
    return Course.query.all()


class PaymentForm(FlaskForm):
    student_email = EmailField(_l('Student email'), validators=[required()])
    total = IntegerField(_l('Total'), validators=[required()])
    course_name = QuerySelectField(_l('Course name'), validators=[required()], query_factory=course_list)
    type_of_class = SelectField(_l('Type of class'), choices=type_of_class)
    payment_for_month = SelectField(_l('Payment for'), choices=month_name_list)
    status_of_payment = SelectField(_l('Payment Status'), choices=payment_status)
    submit = SubmitField()

    def validate_student_email(self, field):
        if Student.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('It seems the email is not registered as a student email.'))
