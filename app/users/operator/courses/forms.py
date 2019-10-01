from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms.fields import StringField, SubmitField, FileField
from wtforms import ValidationError
from wtforms.validators import InputRequired, Length

from app.models import Course


class AddCourseForm(FlaskForm):
    name = StringField(_l('Course name'), validators=[InputRequired(), Length(1, 100)])
    image = FileField(_l('Image'), validators=[InputRequired()])
    submit = SubmitField(_l('Add course'))

    def validate_name(form, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError(_('Course name already registered!'))


class EditCourseForm(FlaskForm):
    name = StringField(_l('Course name'), validators=[InputRequired(), Length(1, 100)])
    image = FileField(_l('Image'), validators=[InputRequired()])
    submit = SubmitField(_l('Edit course'))
