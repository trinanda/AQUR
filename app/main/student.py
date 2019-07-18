from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import student_required

student = Blueprint('student', __name__)


@student.route('/')
@login_required
@student_required
def index():
    return render_template('main/student/index.html')
