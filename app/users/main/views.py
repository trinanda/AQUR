from flask import Blueprint, render_template, url_for, flash
from werkzeug.utils import redirect

from app.models import EditableHTML, Role, Student, User, RequisitionSchedule, TimeSchedule, Course, \
    RequisitionScheduleStatus
from flask_babel import _
from app import db
from app.users.main.forms import OneStepForm

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    # redirect to login page until the homepage feature available
    # return redirect(url_for('account.login'))
    return render_template('main/index.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)


@main.route('/form', methods=['POST', 'GET'])
def one_step_form():
    set_defatul_student_role = Role.query.filter_by(index='student').first()
    form = OneStepForm()
    if form.validate_on_submit():
        first_name = str(form.first_name.data)
        last_name = str(form.last_name.data)

        # TODO | InsyaAllah will working in the line bellow | what if user doesn't have email..?
        email = form.email.data
        if email is None:
            number = 0
            while True:
                number += 1
                if User.query.filter_by(email=email).first is not None:
                    email = "".join(first_name.split()) + "".join(last_name.split()) + str(number) + '@gmail.com'
                else:
                    return False

        student = Student(
            role=set_defatul_student_role,
            first_name=first_name,
            last_name=last_name,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            address=form.address.data,
            email=email,
            phone_number=form.phone_number.data,
            password='1',  # TODO | set all password to '1' before the student login feature available
            confirmed=True,
        )
        db.session.add(student)

        list_of_dict_time_schedule = []
        for entry in form.time_schedule:
            list_of_dict_time_schedule.append(
                {'day': entry.data['day'], 'time': entry.data['time'].strftime('%H:%M')})

        course = Course.query.filter_by(name=str(form.course_name.data)).first()

        requisition_schedule = RequisitionSchedule(
            student_id=student.id,
            course_id=course.id,
            type_of_class=form.type_of_class.data,
            how_many_times_in_a_week=2,
            requisition_status=RequisitionScheduleStatus.STUDENT_REQUISITION.name,
            note=form.description.data,
        )

        for data in list_of_dict_time_schedule:
            time_schedule = TimeSchedule(day=data['day'], start_at=data['time'])
            requisition_schedule.time_schedule.append(time_schedule)

        db.session.add(requisition_schedule)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('main.one_step_form'))
        flash(_('Successfully added new data'), 'success')
        return redirect(url_for('main.one_step_form'))
    return render_template('main/one-step-form.html', form=form)
