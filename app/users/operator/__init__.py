from flask import Blueprint

operator = Blueprint('operator', __name__)

from app.users.operator import courses_views
from app.users.operator import views
