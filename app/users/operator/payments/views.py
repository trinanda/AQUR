from flask import render_template, flash, url_for, abort
from flask_login import login_required
from werkzeug.utils import redirect

from app import db
from app.decorators import operator_required
from app.models import Payment, Student, Course
from app.users.operator import operator
from app.users.operator.payments.forms import PaymentForm


@operator.route('/all-payments')
@login_required
@operator_required
def all_payments():
    payments = db.session.query(Payment.id, Payment.type_of_class, Payment.total, Payment.payment_for_month,
                                Payment.status_of_payment, Payment.created_at, Payment.updated_at, Student.email,
                                Payment.type_of_class, Course.name, Student.full_name).join(Student, Course).order_by(
        Payment.updated_at.desc()).all()

    return render_template('main/operator/payments/all-payments.html', payments=payments)


@operator.route('/payment/add-payment', methods=['GET', 'POST'])
@login_required
@operator_required
def add_payment():
    """Create a new payments."""
    form = PaymentForm()
    if form.validate_on_submit():
        student_email = form.student_email.data
        student_id = db.session.query(Student.id).filter_by(email=student_email).first()

        course_name = str(form.course_name.data)
        course_id = db.session.query(Course.id).filter_by(name=course_name).first()

        payments = Payment(
            student_id=student_id,
            total=form.total.data,
            course_id=course_id,
            type_of_class=form.type_of_class.data,
            payment_for_month=form.payment_for_month.data,
            status_of_payment=form.status_of_payment.data
        )
        db.session.add(payments)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash('Successfully added new payment', 'success')
        return redirect(url_for('operator.all_payments'))
    return render_template('main/operator/payments/manipulate-payment.html', form=form)


@operator.route('/payment/edit_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
@operator_required
def edit_payment(payment_id):
    """Edit a payment's information."""
    payment = Payment.query.filter_by(id=payment_id).first()

    form = PaymentForm(obj=payment)
    form.course_name.default = lambda: db.query(Course).filter_by(id=payment.course_id).first()
    form.student_email.default = lambda: db.query(Student.email).filter_by(id=payment.student_id).first()

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
        payment.payment_for_month = form.payment_for_month.data
        payment.status_of_payment = form.status_of_payment.data

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash('Successfully edit payment', 'success')
        return redirect(url_for('operator.all_payments'))
    return render_template('main/operator/payments/manipulate-payment.html', payment=payment, form=form)
