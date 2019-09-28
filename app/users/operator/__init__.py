from flask import Blueprint

operator = Blueprint('operator', __name__)

from app.users.operator import views
from app.users.operator.courses import views
from app.users.operator.teachers import views
from app.users.operator.students import views
from app.users.operator.payments import views
from app.users.operator.schedules import views
