from flask import Blueprint, render_template

operator = Blueprint('operator', __name__)


@operator.route('/')
def index():
    return 'hello operator :)'
