from flask import render_template, flash, url_for, request, abort
from flask_login import login_required
from sqlalchemy import or_
from werkzeug.utils import redirect
from flask_babel import _

from app import db, photos
from app.decorators import operator_required
from app.models import Course, MonthNameList, Payment, TypeOfClass, Gender, Student, PaymentStatus
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


@operator.route('/course/course_details/<int:course_id>')
@login_required
@operator_required
def course_details(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)

    # students_payment = db.session.query(Payment, Student).join(Student).distinct(Payment.student_id).filter(
    #     Payment.course_id == course_id)

    # total_students = students_payment.count()
    # total_private_students = students_payment.filter(Payment.type_of_class == TypeOfClass.PRIVATE.value).count()
    # total_regular_students = students_payment.filter(Payment.type_of_class == TypeOfClass.REGULAR.value).count()
    #
    # students_payment_male = students_payment.filter(Student.gender == Gender.Male.value)
    # students_payment_female = students_payment.filter(Student.gender == Gender.Female.value)
    #
    # total_male_student = students_payment_male.count()
    # total_female_student = students_payment_female.count()
    #
    # month_name_list = []
    # for data in MonthNameList:
    #     month_name_list.append(str(data))

    total_male_students_per_month = [{'data': 5}]  # test
    total_female_students_per_month = [{'data': 4}]  # test
    # for data in month_name_list:
    #     # TODO | InsyaAllah will change the "payment_for_month" filter bellow
    #     total_male_students_per_month.append(
    #         {data: students_payment_male.filter(Payment.payment_for_month == data).count()})
    #     total_female_students_per_month.append(
    #         {data: students_payment_female.filter(Payment.payment_for_month == data).count()})

    legend_male = Gender.Male.name
    legend_female = Gender.Female.name

    male_values = []
    female_values = []

    for data in total_male_students_per_month:
        for value in data.values():
            male_values.append(value)

    for data in total_female_students_per_month:
        for value in data.values():
            female_values.append(value)

    # return render_template('main/operator/courses/course-details.html', total_students=total_students,
    #                        total_private_students=total_private_students, total_regular_students=total_regular_students,
    #                        total_male_student=total_male_student, total_female_student=total_female_student,
    #                        male_values=male_values, female_values=female_values, month_name_list=month_name_list,
    #                        legend_male=legend_male, legend_female=legend_female, course=course)
    return render_template('main/operator/courses/course-details.html',
                           male_values=male_values, female_values=female_values,
                           legend_male=legend_male, legend_female=legend_female, course=course)
