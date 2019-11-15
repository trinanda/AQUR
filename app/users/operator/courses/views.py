from collections import defaultdict

from flask import render_template, flash, url_for, request, abort
from flask_login import login_required
from sqlalchemy import and_
from werkzeug.utils import redirect
from flask_babel import _

from app import db, photos
from app.decorators import operator_required
from app.models import Course, MonthNameList, Payment, TypeOfClass, Gender, Student, PaymentStatus, Schedule
from app.users.operator import operator

from app.users.operator.courses.forms import AddCourseForm, EditCourseForm


@operator.route('/all-courses')
@login_required
@operator_required
def all_courses():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    courses = Course.query.order_by(Course.created_at.desc()).paginate(page, per_page, error_out=False)
    return render_template('main/operator/courses/all-courses.html', courses=courses)


@operator.route('/course/add-course', methods=['GET', 'POST'])
@login_required
@operator_required
def add_course():
    """Create a new course."""
    form = AddCourseForm()
    if form.validate_on_submit():
        course_name = form.name.data
        try:
            filename = photos.save(request.files['image'], name="courses/" + course_name + "_course.")
        except Exception as e:
            flash(_('Please input correct image format'), 'error')
            return redirect(url_for('operator.add_course'))
        course = Course(
            name=course_name,
            private_class_charge_per_minutes=form.private_class_charge_per_minutes.data,
            regular_class_charge_per_minutes=form.regular_class_charge_per_minutes.data,
            min_private_class_duration=form.min_private_class_duration.data,
            min_regular_class_duration=form.min_regular_class_duration.data,
            min_private_class_charge_per_meet=form.min_private_class_charge_per_meet.data,
            min_regular_class_charge_per_meet=form.min_regular_class_charge_per_meet.data,
            image=filename)
        db.session.add(course)
        db.session.commit()
        flash(_('successfully added %(course_name)s course.', course_name=course.course_name()), 'success')
        return redirect(url_for('operator.all_courses'))
    return render_template('main/operator/courses/manipulate-course.html', form=form)


@operator.route('/course/delete_course/<int:course_id>')
@login_required
@operator_required
def delete_course(course_id):
    """Delete a user's account."""
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)
    db.session.delete(course)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Ops!, it seems the course already have registered students, we cannot delete it!', 'error')
        return redirect(url_for('operator.course_details', course_id=course_id))
    flash(_('successfully deleted %(course_name)s course.', course_name=course.course_name()), 'success')
    return redirect(url_for('operator.all_courses'))


@operator.route('/course/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_course(course_id):
    """Edit a course's information."""
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    form = EditCourseForm()
    if form.validate_on_submit():
        course_name = form.name.data
        course.name = course_name

        course.private_class_charge_per_minutes = form.private_class_charge_per_minutes.data
        course.regular_class_charge_per_minutes = form.regular_class_charge_per_minutes.data
        course.min_private_class_duration = form.min_private_class_duration.data
        course.min_regular_class_duration = form.min_regular_class_duration.data
        course.min_private_class_charge_per_meet = form.min_private_class_charge_per_meet.data
        course.min_regular_class_charge_per_meet = form.min_regular_class_charge_per_meet.data

        try:
            filename = photos.save(request.files['image'], name="courses/" + course_name + "_course.")
            course.image = filename
        except Exception as e:
            flash(_('Please input correct image format'), 'error')
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash(_('Successfully edit course'), 'success')
        return redirect(url_for('operator.course_details', course_id=course_id))
    return render_template('main/operator/courses/manipulate-course.html', course=course, form=form)


@operator.route('/course/course-details/<int:course_id>')
@login_required
@operator_required
def course_details(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    # get all students data on schedule, except if the student tuition payment is None, PENDING, REJECTED or WARNING_3
    students_courses_data = db.session.query(Schedule, Payment).join(Payment).filter(
        Schedule.course_id == course_id).filter(and_(Payment.status_of_payment is not None,
                                                     Payment.status_of_payment != PaymentStatus.PENDING.name,
                                                     Payment.status_of_payment != PaymentStatus.REJECTED.name,
                                                     Payment.status_of_payment != PaymentStatus.WARNING_3.name))

    # get the amount of students data
    total_students = students_courses_data.distinct(Schedule.student_id).count()
    male_student = students_courses_data.join(Student).filter(Student.gender == Gender.Male.name)
    female_student = students_courses_data.join(Student).filter(Student.gender == Gender.Female.name)
    total_private_students = students_courses_data.distinct(Schedule.student_id).filter(
        Schedule.type_of_class == TypeOfClass.PRIVATE.name).count()
    total_regular_students = students_courses_data.distinct(Schedule.student_id).filter(
        Schedule.type_of_class == TypeOfClass.REGULAR.name).count()
    total_male_student = male_student.distinct(Schedule.student_id).count()
    total_female_student = female_student.distinct(Schedule.student_id).count()

    # extract all payment data that matching to the looping month
    month_name_list = []
    for data in MonthNameList:
        month_name_list.append(data.name)
    total_male_students_per_month_list = []
    total_female_students_per_month_list = []
    for male_data in male_student.all():
        for month_name_data in month_name_list:
            total_male_students_per_month_list.append(
                {month_name_data: [male_data.Payment.created_at.strftime('%B')].count(month_name_data)})
    for female_data in female_student.all():
        for month_name_data in month_name_list:
            total_female_students_per_month_list.append(
                {month_name_data: [female_data.Payment.created_at.strftime('%B')].count(month_name_data)})

    # match the students amount with the looping of month
    total_male_students_per_month = defaultdict(int)
    for d in total_male_students_per_month_list:
        for key, value in d.items():
            total_male_students_per_month[key] += value
    total_female_students_per_month = defaultdict(int)
    for d in total_female_students_per_month_list:
        for key, value in d.items():
            total_female_students_per_month[key] += value

    # storing the amount of students that has paid with matching month on the codes above
    male_values = []
    for key, value in total_male_students_per_month.items():
        male_values.append(value)
    female_values = []
    for key, value in total_female_students_per_month.items():
        female_values.append(value)

    legend_male = Gender.Male.value
    legend_female = Gender.Female.value

    return render_template('main/operator/courses/course-details.html',
                           legend_male=legend_male, legend_female=legend_female, course=course,
                           month_name_list=month_name_list, total_students=total_students,
                           total_male_student=total_male_student, total_female_student=total_female_student,
                           total_private_students=total_private_students, total_regular_students=total_regular_students,
                           male_values=male_values, female_values=female_values)
