from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import StringField, SubmitField, FileField, PasswordField, SelectField
from wtforms import ValidationError
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, required

from app.models import User, Course, gender


def course_list():
    return Course.query.all()


class InviteTeacherForm(Form):
    first_name = StringField('First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(1, 64)])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewTeacherForm(InviteTeacherForm):
    gender = SelectField('Gender', choices=gender)
    taught_courses = QuerySelectMultipleField('Taught course', validators=[required()], query_factory=course_list,
                                              allow_blank=True)
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password2', 'Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Create')


class EditTeacherForm(Form):
    first_name = StringField('First name', )
    last_name = StringField('Last name', validators=[InputRequired(), Length(1, 64)])
    gender = SelectField('Gender', choices=gender)
    date_of_birth = DateField('Date of birth', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address', validators=[InputRequired(), Length(1, 255)])
    photo = FileField('Photo')
    phone_number = StringField('Phone number', validators=[InputRequired(), Length(1, 12)])
    taught_courses = QuerySelectMultipleField('Taught course', validators=[required()], query_factory=course_list)
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Update')

    def validate_phone_number(self, field):
        if User.query.filter_by(phone_number=field.data).first():
            raise ValidationError('Phone number already exist..!')
