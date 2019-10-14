import datetime

from flask import render_template, flash, url_for, request, session
from flask_login import login_required
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from sqlalchemy import or_
from flask_babel import _
from wtforms import FieldList, FormField

from app import db
from app.decorators import operator_required
from app.models import TemporaryPayment, Student, Course, Schedule, Teacher, taught_courses, TimeSchedule, \
    RequisitionSchedule, PaymentStatus, DayNameList
from app.users.operator import operator
from app.users.operator.schedules.forms import ScheduleForm, CheckScheduleForm, TimeScheduleForm, \
    RequisitionScheduleForm


@operator.route('/all-schedules')
@login_required
@operator_required
def all_schedules():
    schedules = db.session.query(Schedule).all()
    return render_template('main/operator/schedules/all-schedules.html', schedules=schedules)


@operator.route('/schedule/add-schedule', methods=['GET', 'POST'])
@login_required
@operator_required
def add_schedule():
    schedule_form = ScheduleForm()

    if "step" not in request.form:
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="input_student_email")

    elif request.form["step"] == "available_course":
        student_email = schedule_form.student_email.data
        session['student_email'] = student_email
        student = db.session.query(TemporaryPayment, Student, Course).join(Student, Course).filter(
            Student.email == student_email).filter(
            or_(TemporaryPayment.status_of_payment == PaymentStatus.INSTALLMENT.value,
                TemporaryPayment.status_of_payment == PaymentStatus.COMPLETED.value)).all()

        for data in student:
            if data.Student.gender is None:
                flash(_('It seems the student biodata not completed!'), 'error')
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
        student_status = db.session.query(TemporaryPayment, Student, Course).join(Student, Course).filter(
            Student.email == student_email).filter(
            or_(TemporaryPayment.status_of_payment == PaymentStatus.INSTALLMENT.value,
                TemporaryPayment.status_of_payment == PaymentStatus.COMPLETED.value)).filter(
            Course.name == course_name).all()

        student_available_type_of_class = []
        for data in student_status:
            student_available_type_of_class.append(
                (data.TemporaryPayment.type_of_class, data.TemporaryPayment.type_of_class))
        schedule_form.course_name.choices = set(student_available_type_of_class)
        schedule_form.type_of_class.choices = student_available_type_of_class
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="type_of_class")

    elif request.form["step"] == "how_many_times_in_a_week":
        session['type_of_class'] = schedule_form.type_of_class.data
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="how_many_times_in_a_week")

    # TODO | InsyaAllah will working in the feature bellow | use the real value from database
    elif request.form["step"] == "input_schedule":
        student_email = session.get('student_email')
        student = Student.query.filter_by(email=student_email).first()
        course_name = session.get('course_name')
        course = Course.query.filter_by(name=course_name).first()
        type_of_class = session.get('type_of_class')

        student_temporary_payment = db.session.query(TemporaryPayment).filter_by(student_id=student.id).filter_by(course_id=course.id).filter_by(type_of_class=type_of_class).first()

        tahsin_private_class_charge_per_minutes = 833  # Rp. per minutes
        tahsin_regular_class_charge_per_minutes = 104  # Rp. per minutes

        tahsin_min_private_class_duration = 30  # minutes
        tahsin_min_regular_class_duration = 90  # minutes

        tahsin_min_private_class_charge_per_meet = 25000  # minutes
        tahsin_regular_class_charge_per_meet = 9375.00000003  # minutes

        tahsin_student_wallet_on_this_course = student_temporary_payment.total  # Rp.
        tahsin_student_remaining_duration_in_minutes = tahsin_student_wallet_on_this_course / tahsin_private_class_charge_per_minutes

        how_many_times_in_a_week = schedule_form.how_many_times_in_a_week.data

        class_duration = tahsin_student_remaining_duration_in_minutes / how_many_times_in_a_week  # in this case = 60 minutes
        max_student_meet_duration = tahsin_student_wallet_on_this_course / tahsin_min_private_class_charge_per_meet

        session['tahsin_private_class_duration_per_minutes'] = tahsin_private_class_charge_per_minutes
        session['tahsin_min_private_class_duration'] = tahsin_min_private_class_duration
        session['tahsin_min_private_class_charge_per_meet'] = tahsin_min_private_class_charge_per_meet
        session['tahsin_student_wallet_on_this_course'] = tahsin_student_wallet_on_this_course
        session['tahsin_student_remaining_duration_in_minutes'] = tahsin_student_remaining_duration_in_minutes
        session['how_many_times_in_a_week'] = how_many_times_in_a_week
        session['class_duration'] = class_duration
        session['max_student_meet_duration'] = max_student_meet_duration

        class LocalTimeScheduleForm(ScheduleForm):
            pass

        LocalTimeScheduleForm.time_schedule = FieldList(FormField(TimeScheduleForm),
                                                        min_entries=how_many_times_in_a_week)
        local_time_schedule_form = LocalTimeScheduleForm()

        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="input_schedule", how_many_times_in_a_week=how_many_times_in_a_week,
                               local_time_schedule_form=local_time_schedule_form)

    elif request.form["step"] == "input_teacher_email":

        time_schedule = []
        for entry in schedule_form.time_schedule:
            time_schedule.append({'day': entry.data['day'], 'start_at': entry.data['start_at'].strftime('%H:%M'),
                                  'end_at': entry.data['end_at'].strftime('%H:%M')})

        course_start_at = str(schedule_form.course_start_at.data)

        session['course_start_at'] = course_start_at
        session['time_schedule'] = time_schedule

        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="input_teacher_email")

    elif request.form["step"] == "check_data":

        time_schedule = session.get('time_schedule')
        student_email = session.get('student_email')
        course_name = session.get('course_name')
        type_of_class = session.get('type_of_class')

        course_start_at = datetime.datetime.strptime((session.get('course_start_at')), '%Y-%m-%d')

        teacher_email = schedule_form.teacher_email.data
        session['teacher_email'] = teacher_email

        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="check_data", student_email=student_email, course_name=course_name,
                               type_of_class=type_of_class, course_start_at=course_start_at,
                               time_schedule=time_schedule, teacher_email=teacher_email)

    elif request.form["step"] == "submit":
        if request.method == "POST":
            student_email = session.get('student_email')
            course_name = session.get('course_name')
            type_of_class = session.get('type_of_class')
            teacher_email = session.get('teacher_email')
            list_of_dict_time_schedule = session.get('time_schedule')
            course_start_at = session.get('course_start_at')

            student = Student.query.filter_by(email=student_email).first()
            course = Course.query.filter_by(name=course_name).first()
            teacher = Teacher.query.filter_by(email=teacher_email).first()
            payment = db.session.query(TemporaryPayment, Student, Course).join(Student, Course).filter(
                Student.id == student.id).filter(Course.name == course_name).first()

            schedule = Schedule(
                payment_id=payment.TemporaryPayment.id,
                student_id=student.id,
                course_id=course.id,
                teacher_id=teacher.id,
                course_start_at=course_start_at
            )

            for data in list_of_dict_time_schedule:
                time_schedule = TimeSchedule(day=data['day'], start_at=data['start_at'], end_at=data['end_at'])
                schedule.time_schedule.append(time_schedule)
            db.session.add(schedule)
            db.session.commit()

            flash(_('Successfully added new schedule for %(student_full_name)s.', student_full_name=student.full_name),
                  'success')
            return redirect(url_for('operator.all_schedules'))
        return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form,
                               step="submit")
    return render_template('main/operator/schedules/manipulate-schedule.html', schedule_form=schedule_form)


@operator.route('/schedule/edit_schedule/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_schedule(schedule_id):
    """Edit a schedule's information."""
    time_schedule = TimeSchedule.query.filter_by(schedule_id=schedule_id).first()
    schedule = Schedule.query.filter_by(id=schedule_id).first()

    if schedule is None:
        abort(404)

    list_prepopulate_schedule_form = []
    for data in schedule.time_schedule:
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

    schedule_form = TimeScheduleForm(obj=schedule)
    try:
        schedule_form.course_name.data = time_schedule.requisition_schedule.course
    except Exception as e:
        schedule_form.course_name.data = None

    schedule_form.schedule_day.data = prepopulate_schedule_form[0]['schedule_day']
    schedule_form.schedule_day_2.data = prepopulate_schedule_form[0]['schedule_day_2']

    if request.method == "POST":
        TimeSchedule.query.filter(TimeSchedule.schedule_id == schedule_id).delete()
        db.session.commit()

        schedule.course_start_at = schedule_form.course_start_at.data

        time_schedule_1 = TimeSchedule(
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

        time_schedule_2 = TimeSchedule(
            day=schedule_day_2,
            start_at=start_at_2,
            end_at=end_at_2,
        )
        schedule.time_schedule.append(time_schedule_1)
        schedule.time_schedule.append(time_schedule_2)
        db.session.add(schedule)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('operator.edit_schedule', schedule_id=schedule_id))
        flash(_('Successfully edit schedule.'), 'success')
        return redirect(url_for('operator.all_schedules'))
    return render_template('main/operator/schedules/manipulate-schedule.html', schedule=schedule,
                           schedule_form=schedule_form, prepopulate_schedule_form=prepopulate_schedule_form)


@operator.route('/schedule/check-schedules', methods=['GET', 'POST'])
@login_required
@operator_required
def check_schedules():
    schedules = db.session.query(Schedule).all()
    form = CheckScheduleForm()

    course_list = []

    for data in Course.query.all():
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

        not_available_teachers_by_schedule = db.session.query(Schedule, TimeSchedule).join(
            TimeSchedule).filter(Schedule.teacher_id.in_(list_of_teachers_id_by_gender),
                                 TimeSchedule.start_at == start_at).filter(
            TimeSchedule.day == schedule_day).all()

        not_available_teachers = []
        for data in not_available_teachers_by_schedule:
            not_available_teachers.append(data.teacher_id)

        available_teachers = db.session.query(Teacher).filter(Teacher.id.in_(list_of_teachers_id_by_gender),
                                                              ~Teacher.id.in_(not_available_teachers)).all()

        return render_template('main/operator/schedules/check-schedules.html', form=form, step="available_teacher",
                               available_teachers=available_teachers)
    return render_template('main/operator/schedules/check-schedules.html', form=form, schedules=schedules)


@operator.route('/schedule/all-requisition-schedules')
@login_required
@operator_required
def requisition_schedules():
    requisition_schedules = RequisitionSchedule.query.all()
    return render_template('main/operator/schedules/requisition-schedules.html',
                           requisition_schedules=requisition_schedules)


@operator.route('/schedule/add-requisition-schedule', methods=['GET', 'POST'])
@login_required
@operator_required
def add_requisition_schedules():
    form = RequisitionScheduleForm()
    if request.method == "POST":
        # TODO | InsyaAllah will check the line bellow | why we can't use validate_on_submit..?
        # if form.validate_on_submit():
        student = Student.query.filter_by(email=form.student_email.data).first()
        if student is None:
            flash(_('It seems the email is not registered as a student email!'), 'error')
            return redirect(url_for('operator.add_requisition_schedules'))

        course = Course.query.filter_by(name=str(form.course_name.data)).first()

        requisition_schedule = RequisitionSchedule(
            student_id=student.id,
            course_id=course.id,
            type_of_class=form.type_of_class.data,
        )
        time_schedule_1 = TimeSchedule(
            day=form.schedule_day.data,
            start_at=form.start_at.data,
            end_at=form.end_at.data,
        )

        schedule_day_2 = request.form['schedule_day_2']
        if schedule_day_2 == ' ':
            schedule_day_2 = None

        start_at_2 = request.form['start_at_2']
        if start_at_2 == '':
            start_at_2 = None

        end_at_2 = request.form['end_at_2']
        if end_at_2 == '':
            end_at_2 = None

        time_schedule_2 = TimeSchedule(
            day=schedule_day_2,
            start_at=start_at_2,
            end_at=end_at_2,
        )

        requisition_schedule.time_schedule.append(time_schedule_1)
        requisition_schedule.time_schedule.append(time_schedule_2)
        db.session.add(requisition_schedule)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('operator.add_requisition_schedules'))
        flash(_('Successfully added new requisition schedule for %(student_full_name)s.',
                student_full_name=student.full_name), 'success')
        return redirect(url_for('operator.requisition_schedules'))
    return render_template('main/operator/schedules/manipulate-requisition-schedules.html', form=form)


@operator.route('/schedule/edit-requisition-schedules/<int:requisition_schedule_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_requisition_schedules(requisition_schedule_id):
    """Edit a requisition_schedule information."""
    time_schedule = TimeSchedule.query.filter_by(requisition_schedule_id=requisition_schedule_id).first()
    requisition_schedule = RequisitionSchedule.query.filter_by(id=requisition_schedule_id).first()

    if time_schedule is None:
        abort(404)
    if requisition_schedule is None:
        abort(404)

    list_prepopulate_requisition_schedule_form = []
    for data in requisition_schedule.time_schedule:
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
    form.course_name.data = time_schedule.requisition_schedule.course

    form.schedule_day.data = prepopulate_requisition_schedule_form[0]['schedule_day']
    form.schedule_day_2.data = prepopulate_requisition_schedule_form[0]['schedule_day_2']

    if request.method == "POST":

        student = Student.query.filter_by(email=form.student_email.data).first()
        if student is None:
            flash(_('It seems the email is not registered as a student email!'), 'error')
            return redirect(
                url_for('operator.edit_requisition_schedules', requisition_schedule_id=requisition_schedule_id))

        requisition_schedule.student_id = student.id
        requisition_schedule.course_id = request.form['course_name']
        requisition_schedule.type_of_class = form.type_of_class.data

        TimeSchedule.query.filter(TimeSchedule.requisition_schedule_id == requisition_schedule_id).delete()
        db.session.commit()

        time_schedule_1 = TimeSchedule(
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

        time_schedule_2 = TimeSchedule(
            day=schedule_day_2,
            start_at=start_at_2,
            end_at=end_at_2,
        )

        requisition_schedule.time_schedule.append(time_schedule_1)
        requisition_schedule.time_schedule.append(time_schedule_2)
        db.session.add(requisition_schedule)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(
                url_for('operator.edit_requisition_schedules', requisition_schedule_id=requisition_schedule_id))
        flash(_('Successfully edit requisition schedule.'), 'success')
        return redirect(url_for('operator.requisition_schedules'))
    return render_template('main/operator/schedules/manipulate-requisition-schedules.html',
                           requisition_schedule=requisition_schedule, form=form,
                           prepopulate_requisition_schedule_form=prepopulate_requisition_schedule_form)
