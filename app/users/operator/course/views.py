from flask import render_template, flash, url_for, request, abort
from werkzeug.utils import redirect

from app import db, photos
from app.models import Course
from app.users.operator import operator

from app.users.operator.course.forms import AddCourseForm, EditCourseForm


@operator.route('/all-courses')
def all_courses():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    courses = Course.query.order_by(Course.created_at.desc()).paginate(page, per_page, error_out=False)

    return render_template('main/operator/courses/all-courses.html', courses=courses)


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
        return redirect(url_for('operator.all_courses'))
    return render_template('main/operator/courses/manipulate-course.html', form=form)


@operator.route('/course_details/<int:course_id>')
def course_details(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('main/operator/courses/course-details.html', values=values, labels=labels, legend=legend,
                           course=course)


@operator.route('/delete_course/<int:course_id>')
def delete_course(course_id):
    """Delete a user's account."""
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)
    db.session.delete(course)
    db.session.commit()
    flash('Successfully deleted course %s.' % course.course_name(), 'success')
    return redirect(url_for('operator.all_courses'))


@operator.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    """Edit a course's information."""
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    form = EditCourseForm()
    if form.validate_on_submit():
        course_name = form.name.data
        course.name = course_name
        try:
            filename = photos.save(request.files['image'], name="courses/" + course_name + "_course.")
            course.image = filename
        except Exception as e:
            flash('Please input correct image format', 'error')
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash('Successfully edit course', 'success')
        return redirect(url_for('operator.course_details', course_id=course_id))
    return render_template('main/operator/courses/manipulate_course.html', course=course, form=form)
