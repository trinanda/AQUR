from flask import render_template, flash, url_for, abort
from flask_login import login_required
from werkzeug.utils import redirect
from flask_babel import _

from app import db
from app.decorators import operator_required
from app.models import TemporaryPayment, Student, Course, RegistrationPayment, PaymentStatus, FixedPayment
from app.scheduler_task import transfer_to_fixed_payment
from app.users.operator import operator
from app.users.operator.payments.forms import AddPaymentForm, edit_registration_payment_form_factory, \
    AddRegistrationPaymentForm, edit_payment_form_factory


@operator.route('/payment/temporary-payments')
@login_required
@operator_required
def temporary_payments():
    temporary_payments = db.session.query(TemporaryPayment.id, TemporaryPayment.type_of_class, TemporaryPayment.total,
                                          TemporaryPayment.status_of_payment,
                                          TemporaryPayment.created_at, TemporaryPayment.updated_at, Student.email,
                                          TemporaryPayment.type_of_class, Course.name, Student.full_name).join(Student,
                                                                                                               Course).order_by(
        TemporaryPayment.updated_at.desc()).all()
    return render_template('main/operator/payments/temporary-payments.html', temporary_payments=temporary_payments)


@operator.route('/payment/fixed-payments')
@login_required
@operator_required
def fixed_payments():
    fixed_payments = db.session.query(FixedPayment.id, FixedPayment.type_of_class, FixedPayment.total,
                                      FixedPayment.status_of_payment,
                                      FixedPayment.created_at, FixedPayment.updated_at, Student.email,
                                      FixedPayment.type_of_class, Course.name, Student.full_name).join(Student,
                                                                                                       Course).order_by(
        TemporaryPayment.updated_at.desc()).all()
    return render_template('main/operator/payments/fixed-payments.html', fixed_payments=fixed_payments)


@operator.route('/payment/add-payment', methods=['GET', 'POST'])
@login_required
@operator_required
def add_payment():
    """Create a new payments."""
    form = AddPaymentForm()
    if form.validate_on_submit():
        student_email = form.student_email.data
        student = Student.query.filter_by(email=student_email).first()

        course_name = str(form.course_name.data)
        course_id = db.session.query(Course.id).filter_by(name=course_name).first()

        registration_payment_status = RegistrationPayment.query.filter_by(student_id=student.id).filter_by(
            course_id=course_id).first()

        if str(registration_payment_status) != PaymentStatus.INSTALLMENT.value and str(
            registration_payment_status) != PaymentStatus.COMPLETED.value:
            flash(_('It seems the student didn\'t pay the registration payment for the %(course_name)s course',
                    course_name=course_name), 'warning')
            return redirect(url_for('operator.add_payment'))

        if db.session.query(TemporaryPayment).filter_by(student_id=student.id).filter_by(
            course=form.course_name.data).filter_by(type_of_class=form.type_of_class.data).first() is not None:
            flash(_('The student has taking the course with same type of class'), 'error')
            return redirect(url_for('operator.add_payment'))

        payments = TemporaryPayment(
            student_id=student.id,
            total=form.total.data,
            course_id=course_id,
            type_of_class=form.type_of_class.data,
            status_of_payment=form.status_of_payment.data
        )
        db.session.add(payments)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash(_('Successfully added new payment.'), 'success')
        return redirect(url_for('operator.temporary_payments'))
    return render_template('main/operator/payments/manipulate-payment.html', form=form)


@operator.route('/payment/edit_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_payment(payment_id):
    """Edit a payment's information."""
    payment = TemporaryPayment.query.filter_by(id=payment_id).first()

    EditPaymentForm = edit_payment_form_factory(default_course_name=str(payment.course))
    form = EditPaymentForm(obj=payment)

    if payment is None:
        abort(404)

    if form.validate_on_submit():
        student_email = form.student_email.data
        student_id = db.session.query(Student.id).filter_by(email=student_email).first()
        payment.student_id = student_id
        payment.total = form.total.data
        course_name = str(form.course_name.data)
        course_id = db.session.query(Course.id).filter_by(name=course_name).first()
        payment.course_id = course_id
        payment.type_of_class = form.type_of_class.data
        payment.status_of_payment = form.status_of_payment.data

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash(_('Successfully edit payment.'), 'success')
        return redirect(url_for('operator.temporary_payments'))
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


@operator.route('/run-tasks')
def run_tasks():
    transfer_to_fixed_payment()

    return 'Scheduled several long running tasks.', 200
