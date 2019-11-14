from flask import render_template, url_for, flash, request, abort
from flask_login import login_required
from flask_rq import get_queue
from sqlalchemy import or_
from werkzeug.utils import redirect
from flask_babel import _

from app import db, photos
from app.decorators import operator_required
from app.email import send_email
from app.models import Teacher, Role, User, Schedule, Gender, PaymentStatus, Payment, TaughtCourse
from app.users.operator import operator
from app.users.operator.teachers.forms import InviteTeacherForm, NewTeacherForm, \
    edit_teacher_form_factory


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
    # the number of students that taught by a teacher
    schedule = db.session.query(Schedule, Payment, Teacher).join(Payment, Teacher).filter(
        Schedule.teacher_id == teacher_id).filter(
        or_(Payment.status_of_payment == PaymentStatus.INSTALLMENT.name,
            Payment.status_of_payment == PaymentStatus.COMPLETED.name))
    list_number_of_students = []
    for data in schedule:
        list_number_of_students.append(
            {str(data.Schedule.course): schedule.filter(Schedule.course == data.Schedule.course).count()})
    number_of_students = []
    for dict_ in list_number_of_students:
        if dict_ not in number_of_students:
            number_of_students.append(dict_)
    # /######################################################

    teacher = Teacher.query.filter_by(id=teacher_id).first()
    if teacher is None:
        abort(404)

    # prepopulate the taught courses by a teacher
    list_of_course_id = []
    for teacher_taught_course in TaughtCourse.query.filter_by(teacher_id=teacher_id).all():
        list_of_course_id.append(teacher_taught_course.course_id)
    EditTeacherForm = edit_teacher_form_factory(list_of_course_id=list_of_course_id)
    form = EditTeacherForm(obj=teacher)

    if form.validate_on_submit():
        teacher_name = teacher.full_name
        teacher.first_name = form.first_name.data
        teacher.last_name = form.last_name.data
        teacher.gender = form.gender.data
        teacher.date_of_birth = form.date_of_birth.data
        teacher.address = form.address.data

        # validate unique/identity data
        validate_user_data = User.query.filter(~User.phone_number.in_([teacher.phone_number])).all()
        all_user_phone_number = []
        all_user_email = []
        for data in validate_user_data:
            all_user_phone_number.append(data.phone_number)
        for data in validate_user_data:
            all_user_email.append(data.email)
        if form.phone_number.data in all_user_phone_number:
            flash(_('Duplicate phone number with the other users, please input different number!'), 'error')
            return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))
        if form.email.data in all_user_email:
            flash(_('Duplicate email with the other users, please input different email!'), 'error')
            return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

        teacher.phone_number = form.phone_number.data
        teacher.email = form.email.data

        try:
            if request.files['photo']:
                filename = photos.save(request.files['photo'], name="teachers/" + teacher_name + "_teacher.")
                teacher.photo = filename
        except Exception as e:
            if teacher.gender == Gender.Male.name:
                flash(_('Please input correct image format!'), 'error')
                return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

        TaughtCourse.query.filter_by(teacher_id=teacher_id).delete()
        db.session.commit()

        for taught_course_data in form.taught_courses.data:
            taught_course = TaughtCourse(course_id=taught_course_data.id)
            teacher.taught_course.append(taught_course)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash(_('Successfully updated %(teacher_full_name)s data.', teacher_full_name=teacher.full_name), 'success')
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
        flash(_('Teacher %(teacher_full_name)s successfully invited.', teacher_full_name=teacher.full_name), 'success')
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
            phone_number=form.phone_number.data,
            password=form.password.data,
        )
        for taught_course_data in form.taught_courses.data:
            taught_course = TaughtCourse(course_id=taught_course_data.id)
            teacher.taught_course.append(taught_course)
        db.session.add(teacher)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('operator.new_teacher'))
        flash(_('Successfully added %(teacher_full_name)s as a Teacher.', teacher_full_name=teacher.full_name),
              'success')
        return redirect(url_for('operator.all_teachers'))
    return render_template('main/operator/teachers/manipulate-teacher.html', form=form)


@operator.route('/all-teachers-table-mode')
@login_required
@operator_required
def all_teachers_table_mode():
    teachers = db.session.query(Teacher).all()
    return render_template('main/operator/teachers/all-teachers-table-mode.html', list_of_teachers=teachers)
