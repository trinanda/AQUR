import datetime
from dateutil.relativedelta import relativedelta
from flask_apscheduler import APScheduler
from app.models import Payment, PaymentStatus

scheduler = APScheduler()


def update_tuition_payment_status():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")
    app = scheduler.app
    with app.app_context():
        payment = Payment.query.all()
        for data in payment:
            payment_created_at = datetime.date(data.created_at.year, data.created_at.month, data.created_at.day)
            one_month_later_after_pay_at = payment_created_at + relativedelta(months=1)
            two_month_later_after_pay_at = payment_created_at + relativedelta(months=2)
            three_month_later_after_pay_at = payment_created_at + relativedelta(months=3)

            if str(one_month_later_after_pay_at) == current_time and \
                str(data.status_of_payment) == PaymentStatus.COMPLETED.value:
                data.status_of_payment = PaymentStatus.WARNING_1.name
            elif str(two_month_later_after_pay_at) == current_time and \
                str(data.status_of_payment) == PaymentStatus.WARNING_1.value:
                data.status_of_payment = PaymentStatus.WARNING_2.name
            elif str(three_month_later_after_pay_at) == current_time and \
                str(data.status_of_payment) == PaymentStatus.WARNING_2.value:
                data.status_of_payment = PaymentStatus.WARNING_3.name

    return str('ok')
