from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, FileField
from wtforms import ValidationError
from wtforms.validators import InputRequired, Length

from app.models import Course


class AddCourseForm(Form):
    name = StringField('Course name', validators=[InputRequired(), Length(1, 100)])
    image = FileField('image', validators=[InputRequired()])
    submit = SubmitField('Add course')

    def validate_name(form, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('Course name already registered!')
