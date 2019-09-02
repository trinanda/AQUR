from flask import render_template

from app.users.operator import operator


@operator.route('/all_students')
def all_students():
    return render_template('main/operator/all-students.html')


@operator.route('/student_profile')
def student_profile():
    return render_template('main/operator/student-profile.html')
