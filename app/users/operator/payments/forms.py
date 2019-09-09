from flask_wtf import Form
from wtforms import SelectField, StringField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from wtforms.validators import required

from app.models import Course, type_of_class, month_name_list, payment_status


def courses():
    return Course.query.all()


class PaymentForm(Form):
    student_email = StringField('Student email')
    total = IntegerField(validators=[required()])
    course_name = QuerySelectField('Course name', validators=[required()], query_factory=courses)
    type_of_class = SelectField('Type of class', choices=type_of_class)
    payment_for_month = SelectField('Payment for', choices=month_name_list)
    status_of_payment = SelectField('Payment Status', choices=payment_status)
    submit = SubmitField()
