from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import teacher_required

teacher = Blueprint('teacher', __name__)


@teacher.route('/')
@login_required
@teacher_required
def index():
    return 'hello teacher :)'
