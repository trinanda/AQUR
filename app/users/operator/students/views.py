from flask import render_template, url_for, flash, request, abort
from flask_rq import get_queue
from werkzeug.utils import redirect

from app import db, photos
from app.email import send_email
from app.models import Role, Student, User
from app.users.operator import operator
from app.users.operator.students.forms import InviteStudentForm, EditStudentForm


@operator.route('/add-student', methods=['GET', 'POST'])
def add_student():
    """Invites a new student to create an account and set their own password."""
    set_defatul_student_role = Role.query.filter_by(index='student').first()
    form = InviteStudentForm()
    if form.validate_on_submit():
        student = Student(
            role=set_defatul_student_role,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            gender=form.gender.data)
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
        flash('Student {} successfully invited'.format(student.full_name()),
              'success')
        return redirect(url_for('operator.all_students'))
    return render_template('main/operator/students/manipulate-student.html', form=form)


@operator.route('/all-students')
def all_students():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    students = Student.query.order_by(Student.created_at.desc()).paginate(page, per_page, error_out=False)
    return render_template('main/operator/students/all-students.html', students=students)


@operator.route('/student-profile/<int:student_id>', methods=['GET', 'POST'])
def student_profile(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if student is None:
        abort(404)

    student_form = EditStudentForm(obj=student)

    if student_form.validate_on_submit():
        student_name = student.full_name
        student.first_name = student_form.first_name.data
        student.last_name = student_form.last_name.data
        student.gender = student_form.gender.data
        student.date_of_birth = student_form.date_of_birth.data
        student.address = student_form.address.data
        student.phone_number = student_form.phone_number.data

        for check_email in db.session.query(User.email).all():
            if student.email == student_form.email.data:
                pass
            elif student_form.email.data in check_email:
                flash('Email already registered', 'error')
                return redirect(url_for('operator.student_profile', student_id=student_id))

        student.email = student_form.email.data

        try:
            if not request.files['photo']:
                pass
            else:
                filename = photos.save(request.files['photo'], name="students/" + student_name + "_student.")
                student.photo = filename
        except Exception as e:
            if student_form.gender.data == "Male":
                return redirect(url_for('operator.student_profile', student_id=student_id))

            flash('Please input correct image format', 'error')
            return redirect(url_for('operator.student_profile', student_id=student_id))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        if student_form.gender.data == "Male" or student_form.gender.data == "Female":
            flash('Successfully updated {}'.format(student.full_name + ' data'), 'success')
        return redirect(url_for('operator.student_profile', student_id=student_id))

    return render_template('main/operator/students/student-profile.html', student=student, student_form=student_form)
