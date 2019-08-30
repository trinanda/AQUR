from flask import render_template

from app.users.operator import operator


@operator.route('/')
# @login_required
# @operator_required
def index():
    return render_template('main/operator/index.html')


@operator.route('/operator_dashboard')
def operator_dashboard():
    return render_template('main/operator/operator-dashboard.html')


@operator.route('/all_teachers')
def all_teachers():
    return render_template('main/operator/all-teachers.html')


@operator.route('/teacher_profile')
def teacher_profile():
    return render_template('main/operator/teacher-profile.html')


@operator.route('/all_students')
def all_students():
    return render_template('main/operator/all-students.html')


@operator.route('/student_profile')
def student_profile():
    return render_template('main/operator/student-profile.html')
