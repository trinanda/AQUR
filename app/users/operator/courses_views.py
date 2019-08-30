from flask import render_template, flash, url_for, request
from werkzeug.utils import redirect

from app import db, photos
from app.models import Course
from app.users.operator import operator

from app.users.operator.forms import AddCourseForm


@operator.route('/courses')
def courses():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    courses = Course.query.order_by(Course.created_at.desc()).paginate(page, per_page, error_out=False)

    return render_template('main/operator/courses/courses.html', courses=courses)


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
    return render_template('main/operator/courses/add_course.html', form=form)
