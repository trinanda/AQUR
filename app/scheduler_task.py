import datetime
import os
import shutil

from dateutil.relativedelta import relativedelta
from flask_apscheduler import APScheduler
from pygdrive3 import service

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
                str(data.status_of_payment) == PaymentStatus.COMPLETED.name:
                data.status_of_payment = PaymentStatus.WARNING_1.name
            elif str(two_month_later_after_pay_at) == current_time and \
                str(data.status_of_payment) == PaymentStatus.WARNING_1.name:
                data.status_of_payment = PaymentStatus.WARNING_2.name
            elif str(three_month_later_after_pay_at) == current_time and \
                str(data.status_of_payment) == PaymentStatus.WARNING_2.name:
                data.status_of_payment = PaymentStatus.WARNING_3.name

    return str('ok')


def backup_db_to_google_drive():
    dir_path = os.path.dirname(os.path.realpath('../config.py')) + '/AQUR/'
    drive_service = service.DriveService(dir_path + 'credentials/client_secrets.json')
    try:
        drive_service.auth()
    except Exception as e:
        return str(e)

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename_to_upload = 'aqur_database_' + current_time

    # remove old files with autoclean command | https://github.com/cuducos/alchemydumps#and-you-can-use-the-auto-clean-command
    os.system('python3 manage.py alchemydumps autoclean')

    # convert directory to zip
    file_to_upload = shutil.make_archive(dir_path + 'save_db_bak/' + filename_to_upload, 'zip',
                                         dir_path + 'alchemydumps')

    # folder name on google drive
    folder = drive_service.create_folder('aqur_db_backup_' + current_time)

    # # upload file (args1=filename_to_upload, args2=file_to_upload, args3=directory_name)
    try:
        file = drive_service.upload_file(filename_to_upload, file_to_upload, folder)
        print('uploaded to to google drive', file)
    except Exception as e:
        return str(e)

    return file
