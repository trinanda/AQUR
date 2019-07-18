from flask import Blueprint, render_template

student = Blueprint('student', __name__)


@student.route('/')
def index():
    return 'hello student, how is it going..?'
