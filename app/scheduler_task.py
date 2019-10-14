import datetime
from dateutil.relativedelta import relativedelta
from flask_apscheduler import APScheduler

from app import db
from app.models import TemporaryPayment, PaymentStatus

scheduler = APScheduler()


def transfer_to_fixed_payment():
    app = scheduler.app
    with app.app_context():

        temporary_payment = TemporaryPayment.query.all()
        utc_now = datetime.datetime.now()

        for data in temporary_payment:
            date_after_month = data.created_at + relativedelta(months=1)

            # if date_after_month == utc_now and data.status_of_payment.value != PaymentStatus.EXPIRED.value:
            # if data.status_of_payment.value != PaymentStatus.EXPIRED.value:
            #     print('yes')
            # else:
            #     print('no')
            # try:
            #     if item.status_of_payment.value != PaymentStatus.EXPIRED.value and date_after_month == utc_now:
            #         print('ya')
            # except Exception as e:
            #     print('no')

            # try:
            #     db.session.commit()
            # except Exception as e:
            #     db.session.rollback()
    return str('ok')
