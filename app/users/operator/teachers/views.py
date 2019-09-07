from flask import render_template, url_for, flash, request, abort
from flask_rq import get_queue
from werkzeug.utils import redirect

from app import db, photos
from app.email import send_email
from app.models import Teacher, Role, User
from app.users.operator import operator
from app.users.operator.teachers.forms import InviteTeacherForm, EditTeacherForm


@operator.route('/add-teacher', methods=['GET', 'POST'])
def add_teacher():
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
        flash('Teacher {} successfully invited'.format(teacher.full_name()),
              'success')
        return redirect(url_for('operator.all_teachers'))
    return render_template('main/operator/teachers/manipulate-teacher.html', form=form)


@operator.route('/all-teachers')
def all_teachers():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    teachers = Teacher.query.order_by(Teacher.created_at.desc()).paginate(page, per_page, error_out=False)
    return render_template('main/operator/teachers/all-teachers.html', teachers=teachers)


@operator.route('/teacher-profile/<int:teacher_id>', methods=['GET', 'POST'])
def teacher_profile(teacher_id):
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    if teacher is None:
        abort(404)

    form = EditTeacherForm()
    if form.validate_on_submit():
        teacher_name = teacher.full_name()
        teacher.first_name = form.first_name.data
        teacher.last_name = form.last_name.data
        teacher.date_of_birth = form.date_of_birth.data
        teacher.address = form.address.data
        teacher.phone_number = form.phone_number.data

        for check_email in db.session.query(User.email).all():
            if teacher.email == form.email.data:
                pass
            elif form.email.data in check_email:
                flash('Email already registered', 'error')
                return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

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
        flash('Successfully updated {}'.format(teacher.full_name() + ' data'), 'success')
        return redirect(url_for('operator.teacher_profile', teacher_id=teacher_id))

    return render_template('main/operator/teachers/teacher-profile.html', teacher=teacher, form=form)
