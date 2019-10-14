from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms.fields import StringField, SubmitField, FileField
from wtforms import ValidationError
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length

from app.models import Course


class AddCourseForm(FlaskForm):
    name = StringField(_l('Course name'), validators=[InputRequired(), Length(1, 100)])
    image = FileField(_l('Course Image'), validators=[InputRequired()])

    private_class_charge_per_minutes = IntegerField(_l('Private class charge per minutes'), validators=[InputRequired()])
    regular_class_charge_per_minutes = IntegerField(_l('Regular class charge per minutes'), validators=[InputRequired()])
    min_private_class_duration = IntegerField(_l('Min private class duration'), validators=[InputRequired()])
    min_regular_class_duration = IntegerField(_l('Min regular class duration'), validators=[InputRequired()])
    min_private_class_charge_per_meet = IntegerField(_l('Min private class charge per meet'), validators=[InputRequired()])
    min_regular_class_charge_per_meet = IntegerField(_l('Min regular class charge per meet'), validators=[InputRequired()])
    submit = SubmitField(_l('Add course'))

    def validate_name(form, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError(_('Course name already registered!'))


class EditCourseForm(FlaskForm):
    name = StringField(_l('Course name'), validators=[InputRequired(), Length(1, 100)])
    image = FileField(_l('Course Image'), validators=[InputRequired()])
    private_class_charge_per_minutes = IntegerField(_l('Private class charge per minutes'), validators=[InputRequired()])
    regular_class_charge_per_minutes = IntegerField(_l('Regular class charge per minutes'), validators=[InputRequired()])
    min_private_class_duration = IntegerField(_l('Min private class duration'), validators=[InputRequired()])
    min_regular_class_duration = IntegerField(_l('Min regular class duration'), validators=[InputRequired()])
    min_private_class_charge_per_meet = IntegerField(_l('Min private class charge per meet'), validators=[InputRequired()])
    min_regular_class_charge_per_meet = IntegerField(_l('Min regular class charge per meet'), validators=[InputRequired()])
    submit = SubmitField(_l('Edit course'))
