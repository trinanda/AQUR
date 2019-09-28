from flask import render_template, url_for, flash, request, abort
from flask_login import login_required
from flask_rq import get_queue
from sqlalchemy import or_
from werkzeug.utils import redirect

from app import db, photos
from app.decorators import operator_required
from app.email import send_email
from app.models import Teacher, Role, User, Course, Schedule, Payment
from app.users.operator import operator
from app.users.operator.teachers.forms import InviteTeacherForm, EditTeacherForm, NewTeacherForm


@operator.route('/all-teachers')
@login_required
@operator_required
def all_teachers():
    page = request.args.get('page', 1, type=int)
    per_page = 100

    teachers = Teacher.query.order_by(Teacher.created_at.desc()).paginate(page, per_page, error_out=False)
    return render_template('main/operator/teachers/all-teachers.html', teachers=teachers)


@operator.route('/teacher/teacher-profile/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def teacher_profile(teacher_id):
    schedule = db.session.query(Schedule, Payment, Course).join(Payment, Course).filter(
        Schedule.teacher_id == teacher_id).filter(
        or_(Payment.status_of_payment == "INSTALLMENT", Payment.status_of_payment == "COMPLETED"))

    list_number_of_students = []
    for data in schedule:
        list_number_of_students.append(
            {str(data.Schedule.course): schedule.filter(Schedule.course == data.Schedule.course).count()})

    number_of_students = []
    for dict_ in list_number_of_students:
        if dict_ not in number_of_students:
            number_of_students.append(dict_)

    teacher = Teacher.query.filter_by(id=teacher_id).first()
    if teacher is None:
        abort(404)

    form = EditTeacherForm(obj=teacher)
    if form.validate_on_submit():
        teacher_name = teacher.full_name
        teacher.first_name = form.first_name.data
        teacher.last_name = form.last_name.data
        teacher.gender = form.gender.data
        teacher.date_of_birth = form.date_of_birth.data
        teacher.address = form.address.data

        validate_user_data = User.query.filter(~User.phone_number.in_([teacher.phone_number])).all()
        all_user_phone_number = []
        all_user_email = []

        for data in validate_user_data:
            all_user_phone_number.append(data.phone_number)

        for data in validate_user_data:
            all_user_email.append(data.email)

        if form.phone_number.data in all_user_phone_number:
            flash('Duplicate phone number with the other users, please input different number', 'error')
            return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

        if form.email.data in all_user_email:
            flash('Duplicate email with the other users, please input different email', 'error')
            return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

        teacher.phone_number = form.phone_number.data
        teacher.email = form.email.data

        try:
            if not request.files['photo']:
                pass
            else:
                filename = photos.save(request.files['photo'], name="teachers/" + teacher_name + "_teacher.")
                teacher.photo = filename
        except Exception as e:
            flash('Please input correct image format', 'error')
            return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        form_taught_courses = []
        for data in form.taught_courses.data:
            form_taught_courses.append(str(data))

        teacher_taught_courses = []
        for data in teacher.taught_courses:
            teacher_taught_courses.append(str(data))

        course_id_1 = db.session.query(Course.id).filter(Course.name.in_(teacher_taught_courses)).all()
        course_id_2 = db.session.query(Course.id).filter(Course.name.in_(form_taught_courses)).all()

        for data in course_id_1:
            course = Course.query.filter_by(id=data).first()
            course.courses.remove(teacher)
            db.session.commit()

        for data in course_id_2:
            course = Course.query.filter_by(id=data).first()
            course.courses.append(teacher)
            db.session.commit()

        flash('Successfully updated {}'.format(teacher.full_name + ' data'), 'success')
        return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

    return render_template('main/operator/teachers/teacher-profile.html', teacher=teacher, form=form,
                           number_of_students=number_of_students)


@operator.route('/teacher/invite-teacher', methods=['GET', 'POST'])
@login_required
@operator_required
def invite_teacher():
    """Invites a new teacher to create an account and set their own password."""
    set_defatul_teacher_role = Role.query.filter_by(index='teacher').first()
    form = InviteTeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(
            role=set_defatul_teacher_role,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(teacher)
        db.session.commit()
        token = teacher.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=teacher.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=teacher.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=teacher,
            invite_link=invite_link,
        )
        flash('Teacher {} successfully invited'.format(teacher.full_name),
              'success')
        return redirect(url_for('operator.all_teachers'))
    return render_template('main/operator/teachers/manipulate-teacher.html', form=form)


@operator.route('/teacher/new-teacher', methods=['GET', 'POST'])
@login_required
@operator_required
def new_teacher():
    set_defatul_teacher_role = Role.query.filter_by(index='teacher').first()
    form = NewTeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(
            role=set_defatul_teacher_role,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(teacher)

        form_taught_courses = form.taught_courses.data
        taught_courses = []
        for data in form_taught_courses:
            taught_courses.append(str(data))

        course_id = db.session.query(Course.id).filter(Course.name.in_(taught_courses)).all()

        for data in course_id:
            course = Course.query.filter_by(id=data).first()
            course.courses.append(teacher)
            db.session.add(course)
            db.session.commit()

        flash('successfully added {} as a Teacher'.format(teacher.full_name),
              'success')
        return redirect(url_for('operator.all_teachers'))
    return render_template('main/operator/teachers/manipulate-teacher.html', form=form)
