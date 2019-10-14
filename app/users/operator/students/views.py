from flask import render_template, url_for, flash, request, abort
from flask_login import login_required
from flask_rq import get_queue
from werkzeug.utils import redirect
from flask_babel import _

from app import db, photos
from app.decorators import operator_required
from app.email import send_email
from app.models import Role, Student, User, Schedule, TemporaryPayment
from app.users.operator import operator
from app.users.operator.students.forms import InviteStudentForm, EditStudentForm, NewStudentForm


@operator.route('/all-students')
@login_required
@operator_required
def all_students():
    page = request.args.get('page', 1, type=int)
    per_page = 100

    students = Student.query.order_by(Student.created_at.desc()).paginate(page, per_page, error_out=False)
    return render_template('main/operator/students/all-students.html', students=students)


@operator.route('/student/student-profile/<int:student_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def student_profile(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if student is None:
        abort(404)

    form = EditStudentForm(obj=student)

    if form.validate_on_submit():
        student_name = student.full_name
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.gender = form.gender.data
        student.date_of_birth = form.date_of_birth.data
        student.address = form.address.data

        validate_user_data = User.query.filter(~User.phone_number.in_([student.phone_number])).all()
        all_user_phone_number = []
        all_user_email = []

        for data in validate_user_data:
            all_user_phone_number.append(data.phone_number)

        for data in validate_user_data:
            all_user_email.append(data.email)

        if form.phone_number.data in all_user_phone_number:
            flash(_('Duplicate phone number with the other users, please input different number!'), 'error')
            return redirect(url_for('operator.student_profile', student_id=student_id))

        if form.email.data in all_user_email:
            flash(_('Duplicate email with the other users, please input different email!'), 'error')
            return redirect(url_for('operator.student_profile', student_id=student_id))

        student.phone_number = form.phone_number.data
        student.email = form.email.data

        try:
            if request.files['photo']:
                filename = photos.save(request.files['photo'], name="students/" + student_name + "_student.")
                student.photo = filename
        except Exception as e:
            if form.gender.data == "Male":
                return redirect(url_for('operator.student_profile', student_id=student_id))
            flash(_('Please input correct image format!'), 'error')
            return redirect(url_for('operator.student_profile', student_id=student_id))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        if form.gender.data == "Male" or form.gender.data == "Female":
            flash(_('successfully updated %(student_full_name)s data.', student_full_name=student.full_name), 'success')
        return redirect(url_for('operator.student_profile', student_id=student_id))
    return render_template('main/operator/students/student-profile.html', student=student, form=form)


@operator.route('/student/invite-student', methods=['GET', 'POST'])
@login_required
@operator_required
def invite_student():
    """Invites a new student to create an account and set their own password."""
    set_defatul_student_role = Role.query.filter_by(index='student').first()
    form = InviteStudentForm()
    if form.validate_on_submit():
        student = Student(
            role=set_defatul_student_role,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(student)
        db.session.commit()
        token = student.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=student.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=student.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=student,
            invite_link=invite_link,
        )
        flash(_('Student %(student_full_name)s successfully invited.', student_full_name=student.full_name), 'success')
        return redirect(url_for('operator.all_students'))
    return render_template('main/operator/students/manipulate-student.html', form=form)


@operator.route('/student/new-student', methods=['GET', 'POST'])
@login_required
@operator_required
def new_student():
    set_defatul_student_role = Role.query.filter_by(index='student').first()
    form = NewStudentForm()
    if form.validate_on_submit():
        student = Student(
            role=set_defatul_student_role,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(student)
        db.session.commit()

        flash(_('Successfully added %(student_full_name)s as a Student.', student_full_name=student.full_name),
              'success')
        return redirect(url_for('operator.all_students'))
    return render_template('main/operator/students/manipulate-student.html', form=form)


@operator.route('/all-students-table-mode')
@login_required
@operator_required
def all_students_table_mode():
    students = Student.query.all()

    list_of_students = []
    for data in students:
        list_of_students.append(
            {'id': data.id, 'full_name': data.full_name, 'email': data.email, 'phone_number': data.phone_number,
             'course_tuition': db.session.query(Schedule).filter(Schedule.student_id == data.id).all()})

    return render_template('main/operator/students/all-students-table-mode.html', list_of_students=list_of_students)



@operator.route('/tuition-courses-details/<int:student_id>')
@login_required
@operator_required
def tuition_courses_details(student_id):
    student_tuitions = TemporaryPayment.query.filter_by(student_id=student_id).all()
    print('student_tuitions', student_tuitions)
    if student_tuitions is None:
        abort(404)
    return render_template('main/operator/students/tuition-courses-details.html', student_tuitions=student_tuitions)
