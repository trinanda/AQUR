from flask import Blueprint

operator = Blueprint('operator', __name__)

from app.users.operator import views
from app.users.operator.course import views
from app.users.operator.teachers import views
from app.users.operator.students import views
from app.users.operator.schedules import views
