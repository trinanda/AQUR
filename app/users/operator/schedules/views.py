from flask import render_template, flash, url_for, request, session
from flask_login import login_required
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from sqlalchemy import or_
from flask_babel import _
from wtforms import FieldList, FormField

from app import db
from app.decorators import operator_required
from app.models import Student, Course, Schedule, Teacher, TimeSchedule, \
    RequisitionSchedule, PaymentStatus, RegistrationPayment
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
    form = ScheduleForm()
    if "step" not in request.form:
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form,
                               step="input_student_email_or_phone_number")
    elif request.form["step"] == "available_course":
        student_email_or_phone_number = form.student_email_or_phone_number.data
        student_data = Student.query.filter_by(email=student_email_or_phone_number).first()
        if student_data is None:
            student_data = Student.query.filter_by(phone_number=student_email_or_phone_number).first()

        if student_data is None:
            flash(_('It seems the email or phone number is not registered as a student.'), 'error')
            return redirect(url_for('operator.add_schedule'))

        session['student_id'] = student_data.id

        student = db.session.query(RegistrationPayment, Student, Course).join(Student, Course).filter(
            Student.email == student_data.email).filter(
            or_(RegistrationPayment.status_of_payment == PaymentStatus.INSTALLMENT.name,
                RegistrationPayment.status_of_payment == PaymentStatus.COMPLETED.name)).all()

        for data in student:
            if data.Student.gender is None:
                flash(_('It seems the student biodata not completed!'), 'error')
                return redirect(url_for('operator.add_schedule'))

        student_available_course = []
        for data in student:
            student_available_course.append((data.Course.name, data.Course.name))
        form.course_name.choices = set(student_available_course)
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form,
                               step="available_course")

    elif request.form["step"] == "input_schedule":
        course_name = form.course_name.data
        type_of_class = form.type_of_class.data
        how_many_times_in_a_week = form.how_many_times_in_a_week.data

        student_id = session.get('student_id')
        check_student_taking_course = db.session.query(Schedule, Student, Course).join(Student, Course).filter(
            Student.id == student_id).all()
        for data in check_student_taking_course:
            if str(data.Schedule.course) == course_name and str(data.Schedule.type_of_class) == type_of_class:
                flash(_('The student already registered on that course with same type of class'), 'warning')
                return redirect(url_for('operator.add_schedule'))

        session['course_name'] = course_name
        session['type_of_class'] = type_of_class
        session['how_many_times_in_a_week'] = how_many_times_in_a_week

        class LocalTimeScheduleForm(ScheduleForm):
            pass

        LocalTimeScheduleForm.time_schedule = FieldList(
            FormField(TimeScheduleForm, label='------------------------------------------'),
            min_entries=how_many_times_in_a_week)
        local_time_form = LocalTimeScheduleForm()

        return render_template('main/operator/schedules/manipulate-schedule.html', form=form,
                               step="input_schedule", how_many_times_in_a_week=how_many_times_in_a_week,
                               local_time_form=local_time_form)

    elif request.form["step"] == "check_data":
        student_id = session.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        course_name = session.get('course_name')
        type_of_class = session.get('type_of_class')
        course_start_at = form.course_start_at.data
        session['course_start_at'] = course_start_at

        teacher = Teacher.query.filter_by(email=form.teacher_email_or_phone_number.data).first()
        if teacher is None:
            teacher = Teacher.query.filter_by(phone_number=form.teacher_email_or_phone_number.data).first()
        if teacher is None:
            flash(_('It seems the email is not registered as a teacher email!'), 'warning')
            return redirect(url_for('operator.add_schedule'))

        session['teacher_id'] = teacher.id

        time_schedule = []
        for entry in form.time_schedule:
            time_schedule.append({'day': entry.data['day'], 'start_at': entry.data['start_at'].strftime('%H:%M'),
                                  'end_at': entry.data['end_at'].strftime('%H:%M')})

        session['time_schedule'] = time_schedule
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form,
                               step="check_data", course_name=course_name,
                               type_of_class=type_of_class, course_start_at=course_start_at,
                               time_schedule=time_schedule, teacher=teacher, student=student)

    elif request.form["step"] == "submit":
        if request.method == "POST":
            student_id = session.get('student_id')
            course_name = session.get('course_name')
            type_of_class = session.get('type_of_class')
            teacher_id = session.get('teacher_id')
            list_of_dict_time_schedule = session.get('time_schedule')
            course_start_at = session.get('course_start_at')
            how_many_times_in_a_week = session.get('how_many_times_in_a_week')

            student = Student.query.filter_by(id=student_id).first()
            course = Course.query.filter_by(name=course_name).first()

            schedule = Schedule(
                student_id=student_id,
                course_id=course.id,
                teacher_id=teacher_id,
                course_start_at=course_start_at,
                how_many_times_in_a_week=how_many_times_in_a_week,
                type_of_class=type_of_class
            )
            for data in list_of_dict_time_schedule:
                time_schedule = TimeSchedule(day=data['day'], start_at=data['start_at'], end_at=data['end_at'])
                schedule.time_schedule.append(time_schedule)
            db.session.add(schedule)
            db.session.commit()
            flash(_('Successfully added new schedule for %(student_full_name)s.', student_full_name=student.full_name),
                  'success')
            return redirect(url_for('operator.all_schedules'))
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="submit")
    return render_template('main/operator/schedules/manipulate-schedule.html', form=form)


@operator.route('/schedule/edit-schedule/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_schedule(schedule_id):
    """Edit a schedule's information."""
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    if schedule is None:
        abort(404)
    form = ScheduleForm(obj=schedule)

    class LocalTimeScheduleForm(ScheduleForm):
        pass

    LocalTimeScheduleForm.time_schedule = FieldList(
        FormField(TimeScheduleForm, label='------------------------------------------'),
        min_entries=schedule.how_many_times_in_a_week)

    local_time_form = LocalTimeScheduleForm(obj=schedule)

    if request.method == "POST":
        TimeSchedule.query.filter(TimeSchedule.schedule_id == schedule_id).delete()
        db.session.commit()

        teacher = Teacher.query.filter_by(email=form.teacher_email_or_phone_number.data).first()
        if teacher is None:
            teacher = Teacher.query.filter_by(phone_number=form.teacher_email_or_phone_number.data).first()
        if teacher is None:
            flash(_('It seems the email is not registered as a teacher email!'), 'warning')
            return redirect(url_for('operator.edit_schedule'))

        schedule.teacher_id = teacher.id
        schedule.course_start_at = form.course_start_at.data
        list_of_dict_time_schedule = []
        for entry in form.time_schedule:
            list_of_dict_time_schedule.append(
                {'day': entry.data['day'], 'start_at': entry.data['start_at'].strftime('%H:%M'),
                 'end_at': entry.data['end_at'].strftime('%H:%M')})
        for data in list_of_dict_time_schedule:
            time_schedule = TimeSchedule(day=data['day'], start_at=data['start_at'], end_at=data['end_at'])
            schedule.time_schedule.append(time_schedule)
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
                           form=form, local_time_form=local_time_form)


@operator.route('/schedule/edit-schedule-schedule-number-of-day/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_schedule_number_of_day(schedule_id):
    """Edit a schedule's information."""
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    if schedule is None:
        abort(404)
    form = ScheduleForm(obj=schedule)

    if "step" not in request.form:
        return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html', form=form,
                               step="how_many_times_in_a_week")
    elif request.form["step"] == "time_schedule":
        how_many_times_in_a_week = form.how_many_times_in_a_week.data
        session['how_many_times_in_a_week'] = how_many_times_in_a_week

        class LocalTimeScheduleForm(ScheduleForm):
            pass

        LocalTimeScheduleForm.time_schedule = FieldList(
            FormField(TimeScheduleForm, label='------------------------------------------'),
            min_entries=how_many_times_in_a_week)
        local_time_form = LocalTimeScheduleForm()
        return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html', form=form,
                               step="time_schedule", local_time_form=local_time_form)
    elif request.form["step"] == "submit":
        if request.method == "POST":
            TimeSchedule.query.filter(TimeSchedule.schedule_id == schedule_id).delete()
            db.session.commit()
            how_many_times_in_a_week = session.get('how_many_times_in_a_week')
            schedule.how_many_times_in_a_week = how_many_times_in_a_week
            list_of_dict_time_schedule = []
            for entry in form.time_schedule:
                list_of_dict_time_schedule.append(
                    {'day': entry.data['day'], 'start_at': entry.data['start_at'].strftime('%H:%M'),
                     'end_at': entry.data['end_at'].strftime('%H:%M')})
            for data in list_of_dict_time_schedule:
                time_schedule = TimeSchedule(day=data['day'], start_at=data['start_at'], end_at=data['end_at'])
                schedule.time_schedule.append(time_schedule)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('operator.edit_schedule', schedule_id=schedule_id))
            flash(_('Successfully edit schedule.'), 'success')
            return redirect(url_for('operator.all_schedules'))
        return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html', form=form,
                               step="submit")
    return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html', schedule=schedule,
                           form=form)


# @operator.route('/schedule/check-schedules', methods=['GET', 'POST'])
# @login_required
# @operator_required
# def check_schedules():
#     schedules = db.session.query(Schedule).all()
#     form = CheckScheduleForm()
#
#     course_list = []
#     for data in Course.query.all():
#         course_list.append((data.name, data.name))
#
#     if "step" not in request.form:
#         form.course_name.choices = course_list
#         return render_template('main/operator/schedules/check-schedules.html', form=form,
#                                step="input_schedule")
#     elif request.form["step"] == "available_teacher":
#         course_name = form.course_name.data
#         gender = form.gender.data
#         schedule_day = form.schedule_day.data
#         start_at = form.start_at.data
#         end_at = form.end_at.data
#
#         ### get a selected course name
#         course = Course.query.filter_by(name=course_name).first()
#         # then get all teacher id that taught the course name
#         # taught_course = db.session.query(taught_courses).filter_by(course_id=course.id).all()
#         # store all of the teacher id that taught the matching course
#         teachers_id = []
#         # for data in taught_course:
#         #     teachers_id.append(data.teacher_id)
#         # /#####################
#
#         ### get a user gender #######################
#         teachers_id_by_gender = Teacher.query.filter(Teacher.id.in_(teachers_id)).filter(Teacher.gender == gender).all()
#         # store all of the teacher id by matching gender
#         list_of_teachers_id_by_gender = []
#         for data in teachers_id_by_gender:
#             list_of_teachers_id_by_gender.append(data.id)
#         ###/#######################
#
#         not_available_teachers_by_schedule = db.session.query(Schedule, TimeSchedule).join(
#             TimeSchedule).filter(Schedule.teacher_id.in_(list_of_teachers_id_by_gender),
#                                  TimeSchedule.start_at == start_at).filter(
#             TimeSchedule.day == schedule_day).all()
#
#         not_available_teachers = []
#         for data in not_available_teachers_by_schedule:
#             not_available_teachers.append(data.teacher_id)
#
#         available_teachers = db.session.query(Teacher).filter(Teacher.id.in_(list_of_teachers_id_by_gender),
#                                                               ~Teacher.id.in_(not_available_teachers)).all()
#
#         return render_template('main/operator/schedules/check-schedules.html', form=form, step="available_teacher",
#                                available_teachers=available_teachers)
#     return render_template('main/operator/schedules/check-schedules.html', form=form, schedules=schedules)


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

    if "step" not in request.form:
        return render_template('main/operator/schedules/manipulate-requisition-schedules.html', form=form,
                               step="how_many_times_in_a_week")
    elif request.form["step"] == "input_student":
        how_many_times_in_a_week = form.how_many_times_in_a_week.data
        session['how_many_times_in_a_week'] = how_many_times_in_a_week

        class LocalTimeScheduleForm(ScheduleForm):
            pass

        LocalTimeScheduleForm.time_schedule = FieldList(
            FormField(TimeScheduleForm, label='------------------------------------------'),
            min_entries=how_many_times_in_a_week)
        local_time_form = LocalTimeScheduleForm()
        return render_template('main/operator/schedules/manipulate-requisition-schedules.html', form=form,
                               step="input_student", local_time_form=local_time_form)

    elif request.form["step"] == "submit":
        if request.method == "POST":
            student = Student.query.filter_by(email=form.student_email_or_phone_number.data).first()
            if student is None:
                student = Student.query.filter_by(phone_number=form.student_email_or_phone_number.data).first()
            if student is None:
                flash(_('It seems the email is not registered as a student email!'), 'warning')
                return redirect(url_for('operator.add_requisition_schedules'))

            course_name = form.course_name.data
            course = Course.query.filter_by(name=str(course_name)).first()
            type_of_class = form.type_of_class.data
            how_many_times_in_a_week = session.get('how_many_times_in_a_week')

            list_of_dict_time_schedule = []
            for entry in form.time_schedule:
                list_of_dict_time_schedule.append(
                    {'day': entry.data['day'], 'start_at': entry.data['start_at'].strftime('%H:%M'),
                     'end_at': entry.data['end_at'].strftime('%H:%M')})

            requisition_schedule = RequisitionSchedule(
                student_id=student.id,
                course_id=course.id,
                type_of_class=type_of_class,
                how_many_times_in_a_week=how_many_times_in_a_week,
            )
            for data in list_of_dict_time_schedule:
                time_schedule = TimeSchedule(day=data['day'], start_at=data['start_at'], end_at=data['end_at'])
                requisition_schedule.time_schedule.append(time_schedule)

            db.session.add(requisition_schedule)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('operator.add_requisition_schedules'))

            flash(_('Successfully added new requistion schedule for %(student_full_name)s.',
                    student_full_name=student.full_name), 'success')
            return redirect(url_for('operator.requisition_schedules'))
        return render_template('main/operator/schedules/manipulate-requisition-schedules.html', form=form,
                               step="submit")
    return render_template('main/operator/schedules/manipulate-requisition-schedules.html', form=form)


@operator.route('/schedule/edit-requisition-schedules/<int:requisition_schedule_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_requisition_schedules(requisition_schedule_id):
    """Edit a schedule's information."""
    requisition_schedule = RequisitionSchedule.query.filter_by(id=requisition_schedule_id).first()
    if requisition_schedule is None:
        abort(404)
    form = RequisitionScheduleForm(obj=requisition_schedule)

    class LocalTimeScheduleForm(ScheduleForm):
        pass

    LocalTimeScheduleForm.time_schedule = FieldList(
        FormField(TimeScheduleForm, label='------------------------------------------'),
        min_entries=requisition_schedule.how_many_times_in_a_week)

    local_time_form = LocalTimeScheduleForm(obj=requisition_schedule)

    if request.method == "POST":
        TimeSchedule.query.filter(TimeSchedule.requisition_schedule_id == requisition_schedule_id).delete()
        db.session.commit()
        list_of_dict_time_schedule = []
        for entry in form.time_schedule:
            list_of_dict_time_schedule.append(
                {'day': entry.data['day'], 'start_at': entry.data['start_at'].strftime('%H:%M'),
                 'end_at': entry.data['end_at'].strftime('%H:%M')})
        for data in list_of_dict_time_schedule:
            time_schedule = TimeSchedule(day=data['day'], start_at=data['start_at'], end_at=data['end_at'])
            requisition_schedule.time_schedule.append(time_schedule)
        db.session.add(requisition_schedule)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(
                url_for('operator.edit_requisition_schedules', requisition_schedule_id=requisition_schedule_id))
        flash(_('Successfully edit schedule.'), 'success')
        return redirect(url_for('operator.requisition_schedules'))
    return render_template('main/operator/schedules/manipulate-requisition-schedules.html',
                           requisition_schedule=requisition_schedule, form=form, local_time_form=local_time_form)


@operator.route('/schedule/edit-requisition-schedule-number-of-day/<int:requisition_schedule_id>',
                methods=['GET', 'POST'])
@login_required
@operator_required
def edit_requisition_schedule_number_of_day(requisition_schedule_id):
    """Edit a schedule's information."""
    requisition_schedule = RequisitionSchedule.query.filter_by(id=requisition_schedule_id).first()
    if requisition_schedule is None:
        abort(404)
    form = RequisitionScheduleForm(obj=requisition_schedule)

    if "step" not in request.form:
        return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html', form=form,
                               step="how_many_times_in_a_week")
    elif request.form["step"] == "time_schedule":
        how_many_times_in_a_week = form.how_many_times_in_a_week.data
        session['how_many_times_in_a_week'] = how_many_times_in_a_week

        class LocalTimeScheduleForm(ScheduleForm):
            pass

        LocalTimeScheduleForm.time_schedule = FieldList(
            FormField(TimeScheduleForm, label='------------------------------------------'),
            min_entries=how_many_times_in_a_week)
        local_time_form = LocalTimeScheduleForm()
        return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html', form=form,
                               step="time_schedule", local_time_form=local_time_form)
    elif request.form["step"] == "submit":
        if request.method == "POST":
            TimeSchedule.query.filter(TimeSchedule.requisition_schedule_id == requisition_schedule_id).delete()
            db.session.commit()
            how_many_times_in_a_week = session.get('how_many_times_in_a_week')
            requisition_schedule.how_many_times_in_a_week = how_many_times_in_a_week
            list_of_dict_time_schedule = []
            for entry in form.time_schedule:
                list_of_dict_time_schedule.append(
                    {'day': entry.data['day'], 'start_at': entry.data['start_at'].strftime('%H:%M'),
                     'end_at': entry.data['end_at'].strftime('%H:%M')})
            for data in list_of_dict_time_schedule:
                time_schedule = TimeSchedule(day=data['day'], start_at=data['start_at'], end_at=data['end_at'])
                requisition_schedule.time_schedule.append(time_schedule)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
                return redirect(
                    url_for('operator.edit_requisition_schedules', requisition_schedule_id=requisition_schedule_id))
            flash(_('Successfully edit schedule.'), 'success')
            return redirect(url_for('operator.requisition_schedules'))
        return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html', form=form,
                               step="submit")
    return render_template('main/operator/schedules/manipulate-schedule-number-of-day.html',
                           requisition_schedule=requisition_schedule, form=form)
