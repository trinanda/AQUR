from flask_wtf import FlaskForm
from wtforms import FieldList, FormField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import required
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms import ValidationError, TextAreaField
from wtforms.fields.html5 import EmailField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User, gender, Course, type_of_class, day_name_list


class TimeScheduleForm(FlaskForm):
    day = SelectField(_l('Day'), validators=[required()], choices=day_name_list)
    time = TimeField(_l('Time'), validators=[required()])


class OneStepForm(FlaskForm):
    first_name = StringField(_l('First name'), validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(_l('Last name'), validators=[InputRequired(), Length(1, 64)])
    date_of_birth = DateField(_l('Date of birth'), validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField(_l('Address'), validators=[InputRequired(), Length(1, 255)])
    gender = SelectField(_l('Gender'), choices=gender)
    email = EmailField(_l('Email'))
    phone_number = StringField(_l('Phone number, e.g: 081234567890'), validators=[InputRequired(), Length(1, 12)])
    course_name = QuerySelectField(_l('Course name'),
                                   validators=[required('It seems the student didn\' pay any course ')],
                                   query_factory=lambda: Course.query.all())
    type_of_class = SelectField(_l('Type of class'), validators=[required()], choices=type_of_class)
    time_schedule = FieldList(FormField(TimeScheduleForm, label=''), min_entries=2, label='')
    description = TextAreaField(_l('Reason'), validators=[required()])
    submit = SubmitField()

    def validate_phone_number(self, field):
        if User.query.filter_by(phone_number=field.data).first():
            raise ValidationError(_('Duplicate phone number with the other users in this system, '
                                    'please input different phone number!'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() and not field.data == "":
            raise ValidationError(_('Email already registered.'))
