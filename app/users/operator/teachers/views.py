from flask import render_template, url_for, flash, request
from flask_rq import get_queue
from werkzeug.utils import redirect

from app import db
from app.email import send_email
from app.models import Teacher, Role
from app.users.operator import operator
from app.users.operator.teachers.forms import InviteTeacherForm


@operator.route('/add-teacher', methods=['GET', 'POST'])
def add_teacher():
    """Invites a new teacher to create an account and set their own password."""
    set_defatul_teacher_role = Role.query.filter_by(index='teacher').first()
    print('test role', set_defatul_teacher_role)
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


@operator.route('/teacher-profile')
def teacher_profile():
    return render_template('main/operator/teacher-profile.html')
