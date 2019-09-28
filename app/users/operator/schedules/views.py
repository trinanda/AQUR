import datetime

from flask import render_template, flash, url_for, request, session
from flask_login import login_required
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from sqlalchemy import or_

from app import db
from app.decorators import operator_required
from app.models import Payment, Student, Course, Schedule, Teacher, taught_courses, CourseStatus, ScheduleDayAndTime, \
    RequisitionSchedule
from app.users.operator import operator
from app.users.operator.schedules.forms import ScheduleForm, CheckScheduleForm, ScheduleDayForm, \
    RequisitionScheduleForm


@operator.route('/all-schedules')
@login_required
@operator_required
def all_schedules():
    schedules = db.session.query(Schedule).all()
    return render_template('main/operator/schedules/all-schedules.html', schedules=schedules)


@operator.route('/add-schedule', methods=['GET', 'POST'])
@login_required
@operator_required
def add_schedule():
    schedule_form = ScheduleForm()
    schedule_day_form = ScheduleDayForm()
    if "step" not in request.form:
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="input_student_email")

    elif request.form["step"] == "available_course":
        student_email = schedule_form.student_email.data
        session['student_email'] = student_email
        student = db.session.query(Payment, Student, Course).join(Student, Course).filter(
            Student.email == student_email).filter(
            or_(Payment.status_of_payment == "INSTALLMENT", Payment.status_of_payment == "COMPLETED")).all()

        for data in student:
            if data.Student.gender is None:
                flash('It seems the student biodata not completed.', 'error')
                return redirect(url_for('operator.add_schedule'))

        student_available_course = []
        for data in student:
            student_available_course.append((data.Course.name, data.Course.name))
        schedule_form.course_name.choices = set(student_available_course)
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="available_course")

    elif request.form["step"] == "type_of_class":
        course_name = str(schedule_form.course_name.data)
        session['course_name'] = course_name
        student_email = session.get('student_email')
        student_status = db.session.query(Payment, Student, Course).join(Student, Course).filter(
            Student.email == student_email).filter(
            or_(Payment.status_of_payment == "INSTALLMENT", Payment.status_of_payment == "COMPLETED")).filter(
            Course.name == course_name).all()

        student_available_type_of_class = []
        for data in student_status:
            student_available_type_of_class.append((data.Payment.type_of_class, data.Payment.type_of_class))
        schedule_form.course_name.choices = set(student_available_type_of_class)
        schedule_form.type_of_class.choices = student_available_type_of_class
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               schedule_day_form=schedule_day_form, step="type_of_class")

    elif request.form["step"] == "input_schedule":
        session['type_of_class'] = schedule_form.type_of_class.data
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               schedule_day_form=schedule_day_form, step="input_schedule")

    elif request.form["step"] == "input_teacher_email":
        schedule_day = schedule_day_form.schedule_day.data
        schedule_day_2 = schedule_day_form.schedule_day_2.data
        start_at = str(schedule_day_form.start_at.data)
        start_at_2 = str(schedule_day_form.start_at_2.data)
        end_at = str(schedule_day_form.end_at.data)
        end_at_2 = str(schedule_day_form.end_at_2.data)

        session['schedule_day'] = schedule_day
        session['schedule_day_2'] = schedule_day_2
        session['start_at'] = start_at
        session['start_at_2'] = start_at_2
        session['end_at'] = end_at
        session['end_at_2'] = end_at_2

        # student_email = session.get('student_email')
        # course_name = session.get('course_name')

        ### get a selected course name
        # course = Course.query.filter_by(name=course_name).first()
        # # then get all teacher id that taught the course name
        # taught_course = db.session.query(taught_courses).filter_by(course_id=course.id).all()
        # # store all of the teacher id that taught the matching course
        # teachers_id = []
        # for data in taught_course:
        #     teachers_id.append(data.teacher_id)
        # /#####################

        ### get a user gender #######################
        # student = db.session.query(Student).filter_by(email=student_email).first()
        # teachers_id_by_gender = Teacher.query.filter(Teacher.id.in_(teachers_id)).filter(
        #     Teacher.gender == student.gender.value).all()
        # # store all of the teacher id by matching gender
        # list_of_teachers_id_by_gender = []
        # for data in teachers_id_by_gender:
        #     list_of_teachers_id_by_gender.append(data.id)
        ###/#######################

        # not_available_teachers_by_schedule = Schedule.query.filter(
        #     Schedule.teacher_id.in_(list_of_teachers_id_by_gender), Schedule.start_at == start_at).filter(
        #     Schedule.schedule_day == schedule_day).all()

        # not_available_teachers = []
        # for data in not_available_teachers_by_schedule:
        #     not_available_teachers.append(data.teacher_id)

        # available_teachers = db.session.query(Teacher).filter(Teacher.id.in_(list_of_teachers_id_by_gender),
        #                                                       ~Teacher.id.in_(not_available_teachers)).all()

        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="input_teacher_email")

    elif request.form["step"] == "check_data":
        student_email = session.get('student_email')
        course_name = session.get('course_name')
        type_of_class = session.get('type_of_class')

        schedule_day = session.get('schedule_day')
        start_at = datetime.datetime.strptime(session.get('start_at'), '%H:%M:%S')
        end_at = datetime.datetime.strptime(session.get('end_at'), '%H:%M:%S')

        # schedule_day_2 = session.get('schedule_day_2')
        # start_at_2 = datetime.datetime.strptime(session.get('start_at_2'), '%H:%M:%S')
        # end_at_2 = datetime.datetime.strptime(session.get('end_at_2'), '%H:%M:%S')
        schedule_day_2 = session.get('schedule_day_2')

        try:
            start_at_2 = datetime.datetime.strptime(session.get('start_at_2'), '%H:%M:%S')
            end_at_2 = datetime.datetime.strptime(session.get('end_at_2'), '%H:%M:%S')
        except ValueError:
            start_at_2 = ''
            end_at_2 = ''

        teacher_email = schedule_form.teacher_email.data
        session['teacher_email'] = teacher_email
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="check_data",
                               student_email=student_email, course_name=course_name, type_of_class=type_of_class,
                               schedule_day=schedule_day, schedule_day_2=schedule_day_2, start_at=start_at,
                               start_at_2=start_at_2, end_at=end_at, end_at_2=end_at_2, teacher_email=teacher_email)

    elif request.form["step"] == "submit":
        if request.method == "POST":
            student_email = session.get('student_email')
            course_name = session.get('course_name')
            type_of_class = session.get('type_of_class')
            teacher_email = session.get('teacher_email')

            schedule_day = session.get('schedule_day')
            start_at = session.get('start_at')
            end_at = session.get('end_at')

            schedule_day_2 = session.get('schedule_day_2')
            if schedule_day_2 == '':
                schedule_day_2 = None

            start_at_2 = session.get('start_at_2')
            if start_at_2 == 'None':
                start_at_2 = None

            end_at_2 = session.get('end_at_2')
            if end_at_2 == 'None':
                end_at_2 = None

            student = Student.query.filter_by(email=student_email).first()
            course = Course.query.filter_by(name=course_name).first()
            teacher = Teacher.query.filter_by(email=teacher_email).first()
            payment = db.session.query(Payment, Student, Course).join(Student, Course).filter(
                Student.id == student.id).filter(Course.name == course_name).first()

            schedule_day_and_time = ScheduleDayAndTime(
                day=schedule_day,
                start_at=start_at,
                end_at=end_at,
            )

            schedule_day_and_time_2 = ScheduleDayAndTime(
                day=schedule_day_2,
                start_at=start_at_2,
                end_at=end_at_2,
            )

            schedule = Schedule(
                payment_id=payment.Payment.id,
                student_id=student.id,
                course_id=course.id,
                type_of_class=type_of_class,
                teacher_id=teacher.id,
                course_status=CourseStatus.PENDING.value
            )
            schedule.schedule_day_and_time.append(schedule_day_and_time)
            schedule.schedule_day_and_time.append(schedule_day_and_time_2)
            db.session.add(schedule)
            db.session.commit()

            flash('Successfully added new schedule for {}'.format(student.full_name), 'success')
            return redirect(url_for('operator.all_schedules'))
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="submit")
    return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form)


@operator.route('/edit_schedule/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_schedule(schedule_id):
    """Edit a schedule's information."""
    schedule_day_and_time = ScheduleDayAndTime.query.filter_by(schedule_id=schedule_id).first()
    schedule = Schedule.query.filter_by(id=schedule_id).first()

    if schedule is None:
        abort(404)

    list_prepopulate_schedule_form = []
    for data in schedule.schedule_day_and_time:
        list_prepopulate_schedule_form.append(data.day)
        list_prepopulate_schedule_form.append(data.start_at)
        list_prepopulate_schedule_form.append(data.end_at)

    try:
        prepopulate_schedule_form = [{
            'schedule_day': str(list_prepopulate_schedule_form[0]),
            'start_at': list_prepopulate_schedule_form[1],
            'end_at': list_prepopulate_schedule_form[2],
            'schedule_day_2': str(list_prepopulate_schedule_form[3]),
            'start_at_2': list_prepopulate_schedule_form[4],
            'end_at_2': list_prepopulate_schedule_form[5],
        }]
    except Exception as e:
        prepopulate_schedule_form = [{
            'schedule_day': None,
            'start_at': None,
            'end_at': None,
            'schedule_day_2': None,
            'start_at_2': None,
            'end_at_2': None,
        }]

    schedule_form = ScheduleDayForm(obj=schedule)
    try:
        schedule_form.course_name.data = schedule_day_and_time.requisition_schedule.course
    except Exception as e:
        schedule_form.course_name.data = None

    schedule_form.schedule_day.data = prepopulate_schedule_form[0]['schedule_day']
    schedule_form.schedule_day_2.data = prepopulate_schedule_form[0]['schedule_day_2']

    if request.method == "POST":
        ScheduleDayAndTime.query.filter(ScheduleDayAndTime.schedule_id == schedule_id).delete()
        db.session.commit()

        schedule.course_status = request.form['course_status']
        schedule_day_and_time_1 = ScheduleDayAndTime(
            day=request.form['schedule_day'],
            start_at=request.form['start_at'],
            end_at=request.form['end_at'],
        )
        schedule_day_2 = request.form['schedule_day_2']
        if schedule_day_2 == '':
            schedule_day_2 = None

        start_at_2 = request.form['start_at_2']
        if start_at_2 == '':
            start_at_2 = None

        end_at_2 = request.form['end_at_2']
        if end_at_2 == '':
            end_at_2 = None

        schedule_day_and_time_2 = ScheduleDayAndTime(
            day=schedule_day_2,
            start_at=start_at_2,
            end_at=end_at_2,
        )
        schedule.schedule_day_and_time.append(schedule_day_and_time_1)
        schedule.schedule_day_and_time.append(schedule_day_and_time_2)
        db.session.add(schedule)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('operator.edit_schedule', schedule_id=schedule_id))
        flash('Successfully edit schedule', 'success')
        return redirect(url_for('operator.all_schedules'))
    return render_template('main/operator/schedules/manipulate-schedule.html', schedule=schedule,
                           schedule_form=schedule_form, prepopulate_schedule_form=prepopulate_schedule_form)


@operator.route('/check-schedules', methods=['GET', 'POST'])
@login_required
@operator_required
def check_schedules():
    schedules = db.session.query(Schedule).all()
    form = CheckScheduleForm()

    courses = Course.query.all()
    course_list = []

    for data in courses:
        course_list.append((data.name, data.name))

    if "step" not in request.form:
        form.course_name.choices = course_list
        return render_template('main/operator/schedules/check-schedules.html', form=form,
                               step="input_schedule")

    elif request.form["step"] == "available_teacher":
        course_name = form.course_name.data
        gender = form.gender.data
        schedule_day = form.schedule_day.data
        start_at = form.start_at.data
        end_at = form.end_at.data

        ### get a selected course name
        course = Course.query.filter_by(name=course_name).first()
        # then get all teacher id that taught the course name
        taught_course = db.session.query(taught_courses).filter_by(course_id=course.id).all()
        # store all of the teacher id that taught the matching course
        teachers_id = []
        for data in taught_course:
            teachers_id.append(data.teacher_id)
        # /#####################

        ### get a user gender #######################
        teachers_id_by_gender = Teacher.query.filter(Teacher.id.in_(teachers_id)).filter(Teacher.gender == gender).all()
        # store all of the teacher id by matching gender
        list_of_teachers_id_by_gender = []
        for data in teachers_id_by_gender:
            list_of_teachers_id_by_gender.append(data.id)
        ###/#######################

        not_available_teachers_by_schedule = Schedule.query.filter(
            Schedule.teacher_id.in_(list_of_teachers_id_by_gender), Schedule.start_at == start_at).filter(
            Schedule.schedule_day == schedule_day).all()

        not_available_teachers = []
        for data in not_available_teachers_by_schedule:
            not_available_teachers.append(data.teacher_id)

        available_teachers = db.session.query(Teacher).filter(Teacher.id.in_(list_of_teachers_id_by_gender),
                                                              ~Teacher.id.in_(not_available_teachers)).all()

        return render_template('main/operator/schedules/check-schedules.html', form=form, step="available_teacher",
                               available_teachers=available_teachers)
    return render_template('main/operator/schedules/check-schedules.html', form=form, schedules=schedules,
                           available_teachers='')


@operator.route('/requisition-schedules')
@login_required
@operator_required
def requisition_schedules():
    requisition_schedules = RequisitionSchedule.query.all()
    return render_template('main/operator/schedules/requisition-schedules.html',
                           requisition_schedules=requisition_schedules)


@operator.route('/add-requisition-schedules', methods=['GET', 'POST'])
@login_required
@operator_required
def add_requisition_schedules():
    form = RequisitionScheduleForm()
    if request.method == "POST":
        # if form.validate_on_submit():
        student = Student.query.filter_by(email=form.student_email.data).first()
        if student is None:
            flash('It seems the email is not registered as a student email..!', 'error')
            return redirect(url_for('operator.add_requisition_schedules'))

        course = Course.query.filter_by(name=str(form.course_name.data)).first()

        requisition_schedule = RequisitionSchedule(
            student_id=student.id,
            course_id=course.id,
            type_of_class=form.type_of_class.data,
        )
        schedule_day_and_time_1 = ScheduleDayAndTime(
            day=form.schedule_day.data,
            start_at=form.start_at.data,
            end_at=form.end_at.data,
        )

        schedule_day_2 = request.form['schedule_day_2']
        if schedule_day_2 == '':
            schedule_day_2 = None

        start_at_2 = request.form['start_at_2']
        if start_at_2 == '':
            start_at_2 = None

        end_at_2 = request.form['end_at_2']
        if end_at_2 == '':
            end_at_2 = None

        schedule_day_and_time_2 = ScheduleDayAndTime(
            day=schedule_day_2,
            start_at=start_at_2,
            end_at=end_at_2,
        )

        requisition_schedule.schedule_day_and_time.append(schedule_day_and_time_1)
        requisition_schedule.schedule_day_and_time.append(schedule_day_and_time_2)
        db.session.add(requisition_schedule)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('operator.add_requisition_schedules'))
        flash('Successfully added new requisition schedule for {}'.format(student.full_name), 'success')
        return redirect(url_for('operator.requisition_schedules'))
    return render_template('main/operator/schedules/manipulate-requisition-schedules.html', form=form)


@operator.route('/edit-requisition-schedules/<int:requisition_schedule_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_requisition_schedules(requisition_schedule_id):
    """Edit a requisition_schedule information."""
    schedule_day_and_time = ScheduleDayAndTime.query.filter_by(requisition_schedule_id=requisition_schedule_id).first()
    requisition_schedule = RequisitionSchedule.query.filter_by(id=requisition_schedule_id).first()

    if schedule_day_and_time is None:
        abort(404)
    if requisition_schedule is None:
        abort(404)

    list_prepopulate_requisition_schedule_form = []
    for data in requisition_schedule.schedule_day_and_time:
        list_prepopulate_requisition_schedule_form.append(data.day)
        list_prepopulate_requisition_schedule_form.append(data.start_at)
        list_prepopulate_requisition_schedule_form.append(data.end_at)

    prepopulate_requisition_schedule_form = [{
        'schedule_day': str(list_prepopulate_requisition_schedule_form[0]),
        'start_at': list_prepopulate_requisition_schedule_form[1],
        'end_at': list_prepopulate_requisition_schedule_form[2],
        'schedule_day_2': str(list_prepopulate_requisition_schedule_form[3]),
        'start_at_2': list_prepopulate_requisition_schedule_form[4],
        'end_at_2': list_prepopulate_requisition_schedule_form[5],
    }]

    form = RequisitionScheduleForm(obj=requisition_schedule)
    form.course_name.data = schedule_day_and_time.requisition_schedule.course

    form.schedule_day.data = prepopulate_requisition_schedule_form[0]['schedule_day']
    form.schedule_day_2.data = prepopulate_requisition_schedule_form[0]['schedule_day_2']

    if request.method == "POST":

        student = Student.query.filter_by(email=form.student_email.data).first()
        if student is None:
            flash('It seems the email is not registered as a student email..!', 'error')
            return redirect(url_for('operator.edit_requisition_schedules', requisition_schedule_id=requisition_schedule_id))

        requisition_schedule.student_id = student.id
        requisition_schedule.course_id = request.form['course_name']
        requisition_schedule.type_of_class = form.type_of_class.data

        ScheduleDayAndTime.query.filter(ScheduleDayAndTime.requisition_schedule_id == requisition_schedule_id).delete()
        db.session.commit()

        schedule_day_and_time_1 = ScheduleDayAndTime(
            day=request.form['schedule_day'],
            start_at=request.form['start_at'],
            end_at=request.form['end_at'],
        )
        schedule_day_2 = request.form['schedule_day_2']
        if schedule_day_2 == '':
            schedule_day_2 = None

        start_at_2 = request.form['start_at_2']
        if start_at_2 == '':
            start_at_2 = None

        end_at_2 = request.form['end_at_2']
        if end_at_2 == '':
            end_at_2 = None

        schedule_day_and_time_2 = ScheduleDayAndTime(
            day=schedule_day_2,
            start_at=start_at_2,
            end_at=end_at_2,
        )

        requisition_schedule.schedule_day_and_time.append(schedule_day_and_time_1)
        requisition_schedule.schedule_day_and_time.append(schedule_day_and_time_2)
        db.session.add(requisition_schedule)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(
                url_for('operator.edit_requisition_schedules', requisition_schedule_id=requisition_schedule_id))
        flash('Successfully edit requisition schedule', 'success')
        return redirect(url_for('operator.requisition_schedules'))
    return render_template('main/operator/schedules/manipulate-requisition-schedules.html',
                           requisition_schedule=requisition_schedule, form=form,
                           prepopulate_requisition_schedule_form=prepopulate_requisition_schedule_form)
