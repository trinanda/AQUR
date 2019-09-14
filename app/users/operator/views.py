from flask import render_template

from app.users.operator import operator


@operator.route('/')
# @login_required
# @operator_required
def index():
    return render_template('main/operator/index.html')


@operator.route('/operator-dashboard')
def operator_dashboard():
    return render_template('main/operator/operator-dashboard.html')
