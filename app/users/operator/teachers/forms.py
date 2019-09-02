from flask import url_for
from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import StringField, SubmitField, FileField, PasswordField, DateField, SelectField
from wtforms import ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo

from app import db
from app.models import User, Role
from app.models.selectfield_helpers import LastEducation


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
    name = StringField('Teacher name', validators=[InputRequired(), Length(1, 100)])
    photo = FileField('Image', validators=[InputRequired()])
    submit = SubmitField('Edit course')

# class InviteTeacherForm(Form):
#     gender = QuerySelectField('Gender', validators=[InputRequired()], get_label='name',
#                               query_factory=lambda: db.session.query(Role).order_by('permissions'))
#
#     first_name = StringField('First name', )
#     last_name = StringField('Last name', validators=[InputRequired(), Length(1, 64)])
#     date_of_birth = DateField('Date of birth', validators=[InputRequired()])
#     address = StringField('Address', validators=[InputRequired(), Length(1, 255)])
#     photo = FileField('Photo', validators=[InputRequired()])
#     phone_number = StringField('Phone number', validators=[InputRequired(), Length(1, 12)])
#     email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
#     last_education = SelectField('Last Education',
#                                  choices=[(LastEducation.SD, LastEducation.SD), (LastEducation.SMP, LastEducation.SMP),
#                                           (LastEducation.SMA, LastEducation.SMA), (LastEducation.D1, LastEducation.D1),
#                                           (LastEducation.D2, LastEducation.D2), (LastEducation.D3, LastEducation.D3),
#                                           (LastEducation.S1, LastEducation.S1), (LastEducation.S2, LastEducation.S2),
#                                           (LastEducation.S3, LastEducation.S3)])
#
#     submit = SubmitField('Invite')
#
#     def validate_email(self, field):
#         if User.query.filter_by(email=field.data).first():
#             raise ValidationError('Email already registered.')
