import datetime

from flask import render_template, flash, url_for, abort, request, session
from flask_login import login_required
from werkzeug.utils import redirect
from flask_babel import _

from app import db
from app.decorators import operator_required
from app.models import Student, Course, RegistrationPayment, Payment, Schedule, TypeOfClass
from app.users.operator import operator
from app.users.operator.payments.forms import ManipulatePaymentForm, edit_registration_payment_form_factory, \
    AddRegistrationPaymentForm


@operator.route('/payment/tuition-payments')
@login_required
@operator_required
def tuition_payments():
    tuition_payments = db.session.query(Payment, Schedule).join(Schedule).all()
    return render_template('main/operator/payments/tuition-payments.html', tuition_payments=tuition_payments)


@operator.route('/payment/add-payment', methods=['GET', 'POST'])
@login_required
@operator_required
def add_payment():
    """Create a new payments."""
    form = ManipulatePaymentForm()
    if "step" not in request.form:
        return render_template('main/operator/payments/manipulate-payment.html', form=form, step="input_student_email")
    elif request.form["step"] == "taking_course":
        student_email = form.student_email.data
        student = Student.query.filter_by(email=student_email).first()
        if student is None:
            flash(_('It seems the email is not registered as a student email!'), 'error')
            return redirect(url_for('operator.add_payment'))
        session['student_id'] = student.id
        taking_courses = db.session.query(Schedule).filter(Schedule.student_id == student.id).all()
        return render_template('main/operator/payments/manipulate-payment.html', form=form, step="taking_course",
                               taking_courses=taking_courses)
    elif request.form["step"] == "pay_the_tuition":
        schedule_id = request.form.get("schedule_id")
        session['schedule_id'] = schedule_id
        schedule = Schedule.query.filter_by(id=schedule_id).first()
        if schedule is None:
            return 'schedule is none'
        total_duration_each_month = 0
        for data_time in schedule.time_schedule:
            time_delta = datetime.datetime.strptime(str(data_time.end_at), '%H:%M:%S') - datetime.datetime.strptime(
                str(data_time.start_at), '%H:%M:%S')
            total_duration_in_minutes = time_delta.total_seconds() / 60
            total_duration_each_month += total_duration_in_minutes * 4

        if str(schedule.type_of_class) == TypeOfClass.PRIVATE.value:
            total_charge_per_month = total_duration_each_month * schedule.course.private_class_charge_per_minutes
        else:
            total_charge_per_month = total_duration_each_month * schedule.course.regular_class_charge_per_minutes

        return render_template('main/operator/payments/manipulate-payment.html', form=form, step="pay_the_tuition",
                               schedule=schedule, total_charge_per_month=int(total_charge_per_month))

    elif request.form["step"] == "submit":
        if request.method == "POST":
            student_id = session.get('student_id')
            schedule_id = session.get('schedule_id')
            total = form.total.data
            status_of_payment = form.status_of_payment.data
            schedule = Payment(
                student_id=student_id,
                schedule_id=schedule_id,
                total=total,
                status_of_payment=status_of_payment,
            )
            db.session.add(schedule)
            db.session.commit()
            flash(_('Successfully added payment'), 'success')
            return redirect(url_for('operator.tuition_payments'))
        return render_template('main/operator/schedules/manipulate-schedule.html', form=form, step="submit")
    return render_template('main/operator/payments/manipulate-payment.html', form=form)


@operator.route('/payment/edit_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_payment(payment_id):
    """Edit a payment's information."""
    payment = Payment.query.filter_by(id=payment_id).first()
    form = ManipulatePaymentForm(obj=payment)
    if payment is None:
        abort(404)
    # if form.validate_on_submit():
    if request.method == "POST":
        payment.total = form.total.data
        payment.status_of_payment = form.status_of_payment.data
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash(_('Successfully edit payment.'), 'success')
        return redirect(url_for('operator.tuition_payments'))
    return render_template('main/operator/payments/manipulate-payment.html', payment=payment, form=form)


@operator.route('/payment/registration-payments')
@login_required
@operator_required
def registration_payments():
    registration_payments = RegistrationPayment.query.all()
    return render_template('main/operator/payments/registration-payments.html',
                           registration_payments=registration_payments)


@operator.route('/payment/add-registration-payment', methods=['GET', 'POST'])
@login_required
@operator_required
def add_registration_payment():
    form = AddRegistrationPaymentForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.student_email.data).first()
        course = Course.query.filter_by(name=str(form.course_name.data)).first()

        registration_payment = RegistrationPayment(
            student_id=student.id,
            total=form.total.data,
            course_id=course.id,
            status_of_payment=form.status_of_payment.data
        )
        db.session.add(registration_payment)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash('Success added new registration payment', 'success')
        return redirect(url_for('operator.registration_payments'))
    return render_template('main/operator/payments/manipulate-registration-payment.html', form=form)


@operator.route('/payment/edit-registration-payment/<int:registration_payment_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_registration_payment(registration_payment_id):
    """Edit a registration payment's information."""
    registration_payment = RegistrationPayment.query.filter_by(id=registration_payment_id).first()

    EditRegistrationPaymentForm = edit_registration_payment_form_factory(
        default_course_name=str(registration_payment.course))
    form = EditRegistrationPaymentForm(obj=registration_payment)

    if registration_payments is None:
        abort(404)

    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.student_email.data).first()
        course = Course.query.filter_by(name=str(form.course_name.data)).first()

        registration_payment.student_id = student.id
        registration_payment.course_id = course.id

        registration_payment.total = form.total.data
        registration_payment.status_of_payment = form.status_of_payment.data

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash(_('Successfully edit registration payment.'), 'success')
        return redirect(url_for('operator.registration_payments'))
    return render_template('main/operator/payments/manipulate-registration-payment.html',
                           registration_payment=registration_payment, form=form)
