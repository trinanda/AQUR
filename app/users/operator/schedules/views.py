from flask import render_template

from app.users.operator import operator


# TODO | schedules feature
@operator.route('/all-schedules')
def all_schedules():
    return render_template('main/operator/schedules/all-schedules.html')
