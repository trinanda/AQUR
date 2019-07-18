from flask import Blueprint, render_template

teacher = Blueprint('teacher', __name__)


@teacher.route('/')
def index():
    return 'hello teacher :)'
