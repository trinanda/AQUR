import datetime
from time import sleep

from flask_apscheduler import APScheduler

from app import db
from app.models import TemporaryPayment, Schedule, TypeOfClass

scheduler = APScheduler()


def transfer_to_fixed_payment():
    app = scheduler.app
    with app.app_context():
        TIME_FMT = '%H:%M:%S'
        today = datetime.datetime.utcnow()
        weekday_name = datetime.datetime.today().strftime("%A")
        students_tuitions = db.session.query(Schedule, TemporaryPayment).join(TemporaryPayment).all()
        # students_tuitions = db.session.query(Schedule).all()

        for idx, students_tuition in enumerate(students_tuitions):
            private_class_charge_per_minutes = students_tuition.Schedule.course.private_class_charge_per_minutes
            regular_class_charge_per_minutes = students_tuition.Schedule.course.regular_class_charge_per_minutes
            starting_course_date = datetime.datetime.strptime(str(students_tuition.Schedule.course_start_at), "%Y-%m-%d")

            # print(idx, 'starting_course_date', starting_course_date)
            # print(idx, weekday_name)
            # break

            for schedule_data in students_tuition.Schedule.time_schedule:
                print(schedule_data.start_at, schedule_data.end_at)

            # if students_tuition.TemporaryPayment.type_of_class.value == TypeOfClass.PRIVATE.value:



                # print(idx, students_tuition.TemporaryPayment.type_of_class, students_tuition.TemporaryPayment.total,
                #       starting_course_date)

                # for data_time in students_tuition.Schedule.time_schedule:
                #     start_at = data_time.start_at
                #     end_at = data_time.end_at
                #     time_delta = datetime.datetime.strptime(str(end_at), TIME_FMT) - datetime.datetime.strptime(
                #         str(start_at), TIME_FMT)
                #     total_duration_in_minutes = time_delta.total_seconds() / 60
                #     total_charge = total_duration_in_minutes * private_class_charge_per_minutes

                # for time_schedule_day in students_tuition.Schedule.time_schedule:
                #     if today >= starting_course_date and (weekday_name == str(time_schedule_day.day)):
                        # print(students_tuition.Schedule.student.full_name)

                # for data_time in students_tuition.Schedule.time_schedule:
                #     print(students_tuition.Schedule.student.full_name, data_time.start_at, data_time.end_at)
                #     break

            # for data_time in students_tuition.Schedule.time_schedule:
                #     start_at = data_time.start_at
                #     end_at = data_time.end_at
                #     time_delta = datetime.datetime.strptime(str(end_at), TIME_FMT) - datetime.datetime.strptime(str(start_at), TIME_FMT)
                #     total_duration_in_minutes = time_delta.total_seconds() / 60
                #     total_charge = total_duration_in_minutes * private_class_charge_per_minutes


                    # print(students_tuition.Schedule.student.full_name, total_charge, total_duration_in_minutes, time_delta)
                    # print(students_tuition.Schedule.student.full_name, start_at, end_at)
                    # break


                # for time_schedule_day in students_tuition.Schedule.time_schedule:
                #     # if today >= starting_course_date and (weekday_name == str(time_schedule_day.day)):
                    #     # students_tuition.TemporaryPayment.total -= total_charge




    return str('ok')
# TODO | InsyaAllah will working in this file
