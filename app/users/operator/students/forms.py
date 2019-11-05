from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms.fields import StringField, SubmitField, FileField, PasswordField, SelectField
from wtforms import ValidationError
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

from app.models import User, gender


class InviteStudentForm(FlaskForm):
    first_name = StringField(_l('First name'), validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(_l('Last name'), validators=[InputRequired(), Length(1, 64)])
    email = EmailField(_l('Email'), validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField(_l('Invite'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_('Email already registered.'))


class NewStudentForm(InviteStudentForm):
    phone_number = StringField(_l('Phone number'), validators=[InputRequired(), Length(1, 12)],
                               render_kw={'placeholder': 'e.g: 081234567890'})
    gender = SelectField(_l('Gender'), choices=gender)
    password = PasswordField(_l('Password'),
                             validators=[InputRequired(), EqualTo('password2', 'Passwords must match.')])
    password2 = PasswordField(_l('Confirm password'), validators=[InputRequired()])
    submit = SubmitField(_l('Create'))

    def validate_phone_number(self, field):
        if User.query.filter_by(phone_number=field.data).first():
            raise ValidationError(_('Duplicate phone number with the other users in this system, '
                                    'please input different phone number!'))


class EditStudentForm(FlaskForm):
    first_name = StringField(_l('First name'), validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(_l('Last name'), validators=[InputRequired(), Length(1, 64)])
    email = EmailField(_l('Email'), validators=[InputRequired(), Length(1, 64), Email()])
    gender = SelectField(_l('Gender'), choices=gender)
    phone_number = StringField(_l('Phone number'), validators=[InputRequired(), Length(1, 12)])
    address = StringField(_l('Address'), validators=[InputRequired(), Length(1, 255)])
    date_of_birth = DateField(_l('Date of birth'), validators=[DataRequired()], format='%Y-%m-%d')
    photo = FileField(_l('Photo'))
    submit = SubmitField(_l('Update'))

    def validate_phone_number(self, field):
        if field.data == "None":
            raise ValidationError(_('Please, set the phone number!'))
