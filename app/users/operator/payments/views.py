from flask import render_template, flash, url_for, abort
from werkzeug.utils import redirect

from app import db
from app.models import Payment, Student, Course
from app.users.operator import operator
from app.users.operator.payments.forms import PaymentForm


@operator.route('/all-payments')
def all_payments():
    payments = db.session.query(Payment.type_of_class, Payment.total, Payment.payment_for_month,
                                Payment.status_of_payment, Payment.created_at, Payment.updated_at, Student.email,
                                Payment.type_of_class, Course.name, Student.full_name).join(Student, Course).order_by(
        Payment.updated_at.desc()).all()

    return render_template('main/operator/payments/all-payments.html', payments=payments)


@operator.route('/add-payment', methods=['GET', 'POST'])
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
