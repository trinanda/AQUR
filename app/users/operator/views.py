from flask import Blueprint, render_template, flash, url_for, request
from werkzeug.utils import redirect

from app import db, photos
from app.models import Course

from app.users.operator.forms import AddCourseForm

operator = Blueprint('operator', __name__)


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


@operator.route('/courses')
def courses():
    return render_template('main/operator/courses.html')


@operator.route('/add-course', methods=['GET', 'POST'])
def add_course():
    """Create a new course."""
    form = AddCourseForm()
    if form.validate_on_submit():
        course_name = form.name.data
        try:
            filename = photos.save(request.files['image'], name="courses/" + course_name + "_course.")
        except Exception as e:
            flash('Please input correct image format', 'error')
            return redirect(url_for('operator.add_course'))
        course = Course(
            name=course_name,
            image=filename
        )
        db.session.add(course)
        db.session.commit()
        flash('Successfully added {} '.format(course.course_name()) + 'course', 'success')
        return redirect(url_for('operator.courses'))
    return render_template('main/operator/add_course.html', form=form)
