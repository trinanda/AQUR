from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import StringField, SubmitField, FileField, PasswordField, SelectField
from wtforms import ValidationError
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, required

from app.models import User, Course, gender


def course_list():
    return Course.query.all()


class InviteTeacherForm(FlaskForm):
    first_name = StringField(_l('First name'), validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(_l('Last name'), validators=[InputRequired(), Length(1, 64)])
    email = EmailField(_l('Email'), validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField(_l('Invite'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_('Email already registered.'))


class NewTeacherForm(InviteTeacherForm):
    gender = SelectField(_l('Gender'), choices=gender)
    taught_courses = QuerySelectMultipleField(_l('Taught course'), validators=[required()], query_factory=course_list,
                                              allow_blank=True)
    password = PasswordField(_l('Password'), validators=[InputRequired(), EqualTo('password2', 'Passwords must match.')])
    password2 = PasswordField(_l('Confirm password'), validators=[InputRequired()])
    submit = SubmitField(_l('Create'))


class EditTeacherForm(InviteTeacherForm):
    gender = SelectField(_l('Gender'), choices=gender)
    date_of_birth = DateField(_l('Date of birth'), validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField(_l('Address'), validators=[InputRequired(), Length(1, 255)])
    photo = FileField(_l('Photo'))
    phone_number = StringField(_l('Phone number'), validators=[InputRequired(), Length(1, 12)])
    taught_courses = QuerySelectMultipleField(_l('Taught course'), validators=[required()], query_factory=course_list)
    submit = SubmitField(_l('Update'))

    def validate_phone_number(self, field):
        if field.data == "None":
            raise ValidationError(_('Please, set the phone number!'))
