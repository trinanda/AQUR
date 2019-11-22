from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from app.models import EditableHTML

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    # redirect to login page until the homepage feature available
    return redirect(url_for('account.login'))
    # return render_template('main/index.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
