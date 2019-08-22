from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import operator_required

operator = Blueprint('operator', __name__)


@operator.route('/')
# @login_required
# @operator_required
def index():
    return render_template('main/operator/index.html')


@operator.route('/operator_dashboard')
def operator_dashboard():
    return render_template('main/operator/index.html')


@operator.route('/all_teachers')
def all_teachers():
    return render_template('main/operator/all_teachers.html')


@operator.route('/teacher_profile')
def teacher_profile():
    return render_template('main/operator/teacher_profile.html')
