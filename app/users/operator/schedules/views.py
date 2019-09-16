from flask import render_template, flash, url_for, request, session
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app import db
from app.models import Payment, Student, Course, Schedule, Teacher
from app.users.operator import operator
from app.users.operator.schedules.forms import ScheduleForm

from sqlalchemy import or_


@operator.route('/all-schedules')
def all_schedules():
    schedules = db.session.query(Schedule).all()
    return render_template('main/operator/schedules/all-schedules.html', schedules=schedules)


@operator.route('/add-schedule', methods=['GET', 'POST'])
def add_schedule():
    form = ScheduleForm()
    if "step" not in request.form:
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="input_student_email")

    elif request.form["step"] == "available_course":
        student_email = form.student_email.data
        session['student_email'] = student_email
        student_status = db.session.query(Payment, Student, Course).join(Student, Course).filter(
            Student.email == student_email).filter(
            or_(Payment.status_of_payment == "INSTALLMENT", Payment.status_of_payment == "COMPLETED")).all()
        student_available_course = []
        for data in student_status:
            student_available_course.append((data.Course.name, data.Course.name))
        form.course_name.choices = set(student_available_course)
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="available_course")

    elif request.form["step"] == "type_of_class":
        course_name = str(form.course_name.data)
        session['course_name'] = course_name
        student_email = session.get('student_email')
        student_status = db.session.query(Payment, Student, Course).join(Student, Course).filter(
            Student.email == student_email).filter(
            or_(Payment.status_of_payment == "INSTALLMENT", Payment.status_of_payment == "COMPLETED")).filter(
            Course.name == course_name).all()

        student_available_type_of_class = []
        for data in student_status:
            student_available_type_of_class.append((data.Payment.type_of_class, data.Payment.type_of_class))
        form.course_name.choices = set(student_available_type_of_class)
        form.type_of_class.choices = student_available_type_of_class
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="type_of_class")

    elif request.form["step"] == "input_schedule":
        session['type_of_class'] = form.type_of_class.data
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="input_schedule")

    elif request.form["step"] == "input_teacher_email":
        session['schedule_day'] = form.schedule_day.data
        session['start_at'] = str(form.start_at.data)
        session['end_at'] = str(form.end_at.data)
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form,
                               step="input_teacher_email")

    elif request.form["step"] == "check_data":
        student_email = session.get('student_email')
        course_name = session.get('course_name')
        type_of_class = session.get('type_of_class')
        schedule_day = session.get('schedule_day')
        start_at = session.get('start_at')
        end_at = session.get('end_at')
        teacher_email = form.teacher_email.data
        session['teacher_email'] = teacher_email
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="check_data",
                               student_email=student_email, course_name=course_name, type_of_class=type_of_class,
                               schedule_day=schedule_day, start_at=start_at, end_at=end_at, teacher_email=teacher_email)

    elif request.form["step"] == "submit":
        if request.method == "POST":
            student_email = session.get('student_email')
            course_name = session.get('course_name')
            type_of_class = session.get('type_of_class')
            schedule_day = session.get('schedule_day')
            start_at = session.get('start_at')
            end_at = session.get('end_at')
            teacher_email = session.get('teacher_email')

            student = Student.query.filter_by(email=student_email).first()
            course = Course.query.filter_by(name=course_name).first()
            teacher = Teacher.query.filter_by(email=teacher_email).first()
            payment = db.session.query(Payment, Student, Course).join(Student, Course).filter(
                Student.id == student.id).filter(Course.name == course_name).first()

            schedule = Schedule(
                payment_id=payment.Payment.id,
                student_id=student.id,
                course_id=course.id,
                type_of_class=type_of_class,
                schedule_day=schedule_day,
                start_at=start_at,
                end_at=end_at,
                teacher_id=teacher.id
            )
            db.session.add(schedule)
            db.session.commit()

            flash('Successfully added new schedule for {}'.format(student.full_name), 'success')
            return redirect(url_for('operator.all_schedules'))
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="submit")
    return render_template('main/operator/schedules/manipulate-schedule.html', form=form)


@operator.route('/edit_schedule/<int:schedule_id>', methods=['GET', 'POST'])
def edit_schedule(schedule_id):
    """Edit a schedule's information."""
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    form = ScheduleForm(obj=schedule)

    if schedule is None:
        abort(404)

    if request.method == "POST":
        schedule.schedule_day = form.schedule_day.data
        schedule.start_at = form.start_at.data
        schedule.end_at = form.end_at.data
        schedule.course_status = form.course_status.data

        db.session.commit()
        flash('Successfully edit schedule', 'success')
        return redirect(url_for('operator.all_schedules'))
    return render_template('main/operator/schedules/manipulate-schedule.html', schedule=schedule, form=form)
