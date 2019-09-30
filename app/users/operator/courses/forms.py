from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, FileField
from wtforms import ValidationError
from wtforms.validators import InputRequired, Length

from app.models import Course


class AddCourseForm(FlaskForm):
    name = StringField('Course name', validators=[InputRequired(), Length(1, 100)])
    image = FileField('Image', validators=[InputRequired()])
    submit = SubmitField('Add course')

    def validate_name(form, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('Course name already registered!')


class EditCourseForm(FlaskForm):
    name = StringField('Course name', validators=[InputRequired(), Length(1, 100)])
    image = FileField('Image', validators=[InputRequired()])
    submit = SubmitField('Edit course')
