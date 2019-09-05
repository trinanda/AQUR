from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, FileField, PasswordField
from wtforms import ValidationError
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

from app.models import User


class InviteTeacherForm(Form):
    first_name = StringField('First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(1, 64)])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewTeacherForm(InviteTeacherForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Create')


class EditTeacherForm(Form):
    first_name = StringField('First name', )
    last_name = StringField('Last name', validators=[InputRequired(), Length(1, 64)])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address', validators=[InputRequired(), Length(1, 255)])
    photo = FileField('Photo')
    phone_number = StringField('Phone number', validators=[InputRequired(), Length(1, 12)])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Update')
