from flask import render_template
from flask_login import login_required
from sqlalchemy import or_

from app import db
from app.decorators import operator_required
from app.models import Payment, Student, MonthNameList, Course
from app.users.operator import operator


@operator.route('/')
@login_required
@operator_required
def operator_dashboard():
    title = "AQUR"

    students_payment = db.session.query(Payment, Student, Course).join(Student, Course).filter(
        or_(Payment.status_of_payment == "INSTALLMENT", Payment.status_of_payment == "COMPLETED"))

    ###### total students widgets ################
    total_students = students_payment.count()
    students_per_course = []
    for data in students_payment:
        students_per_course.append({data.Course.name: students_payment.filter(Course.name == data.Course.name).count()})
    total_students_per_course = []
    for dict_ in students_per_course:
        if dict_ not in total_students_per_course:
            total_students_per_course.append(dict_)
    # /###########################################

    month_name_list = []
    for data in MonthNameList:
        month_name_list.append(str(data))

    course = Course.query.all()
    courses_list = []
    for data in course:
        courses_list.append(str(data))

    # TODO | InsyaAllah will work in the feature bellow | make the line bellow can accesible dinamically
    Tahsin_value_per_month = []
    Arabic_language_value_per_month = []
    courses_value = [{"Tahsin": Tahsin_value_per_month, "Arabic Language": Arabic_language_value_per_month}]
    for data in month_name_list:
        data_per_month = students_payment.filter(Payment.payment_for_month == data)

        Tahsin_value_per_month.append(data_per_month.filter(Course.name == "Tahsin").count())
        Arabic_language_value_per_month.append(data_per_month.filter(Course.name == "Arabic Language").count())

    return render_template('main/operator/operator-dashboard.html', title=title, total_students=total_students,
                           month_name_list=month_name_list, total_students_per_course=total_students_per_course,
                           courses_value=courses_value)
