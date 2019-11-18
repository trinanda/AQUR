import os
from collections import defaultdict

from flask import render_template
from flask_login import login_required
from sqlalchemy import and_

from app import db
from app.decorators import operator_required
from app.models import Student, MonthNameList, Course, PaymentStatus, Payment, Teacher, Schedule
from app.users.operator import operator


@operator.route('/')
@login_required
@operator_required
def index():
    title = os.environ.get('APP_NAME')

    # get all students data on schedule, except if the student tuition payment is None, PENDING, REJECTED or WARNING_3
    students_courses_data = db.session.query(Schedule, Payment).join(Payment).filter(
        and_(Payment.status_of_payment is not None,
             Payment.status_of_payment != PaymentStatus.PENDING.name,
             Payment.status_of_payment != PaymentStatus.REJECTED.name,
             Payment.status_of_payment != PaymentStatus.WARNING_3.name))

    # get the amount of Teachers and Students
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()

    month_name_list = []
    for data in MonthNameList:
        month_name_list.append(str(data))

    # make a query object for "Tahsin" and "Arabic Language" course
    tahsin = students_courses_data.join(Course).filter(Course.name == "Tahsin")
    arabic = students_courses_data.join(Course).filter(Course.name == "Bahasa Arab")

    # the total payment for the courses each month
    tahsin_course_data = []
    arabic_course_data = []
    for data in tahsin:
        for month_name in month_name_list:
            tahsin_course_data.append({str(month_name): data.Payment.created_at.strftime('%B').count(month_name)})
    for data in arabic:
        for month_name in month_name_list:
            arabic_course_data.append({str(month_name): data.Payment.created_at.strftime('%B').count(month_name)})

    # merge and sum the total value from the dictionary on the same month from the _courses_data result above
    total_tahsin_students_per_month = defaultdict(int)
    total_arabic_students_per_month = defaultdict(int)
    for d in tahsin_course_data:
        for key, value in d.items():
            total_tahsin_students_per_month[key] += value
    for d in arabic_course_data:
        for key, value in d.items():
            total_arabic_students_per_month[key] += value

    # store all of the month values on a list for each course
    tahsin_values = []
    arabic_values = []
    for key, value in total_tahsin_students_per_month.items():
        tahsin_values.append(value)
    for key, value in total_arabic_students_per_month.items():
        arabic_values.append(value)

    # make a dictionary to represent course name with the matching total student that do the payment for each month
    data_courses_each_month = [
        {
            'Tahsin': tahsin_values,
        },
        {
            'Bahasa Arab': arabic_values
        }
    ]

    return render_template('main/operator/operator-dashboard.html', title=title, total_teachers=total_teachers,
                           total_students=total_students, month_name_list=month_name_list,
                           data_courses_each_month=data_courses_each_month)
