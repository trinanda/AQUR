from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import operator_required

operator = Blueprint('operator', __name__)


@operator.route('/')
@login_required
@operator_required
def index():
    return 'hello operator :)'
