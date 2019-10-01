import os

from flask import Flask, request, current_app
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, UploadSet
from flask_wtf import CSRFProtect
from flask_babel import Babel

from app import cli
from app.assets import app_css, app_js, vendor_css, vendor_js
from config import Config as config_flask_upload
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()
photos = UploadSet('photos', config_flask_upload.UPLOADED_PHOTOS_ALLOW)
babel = Babel()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    Config[config_name].init_app(app)
    register_extensions(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from app.users.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.users.operator import operator as operator_blueprint
    app.register_blueprint(operator_blueprint, url_prefix='/operator')

    from app.users.teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/teacher')

    from app.users.student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/student')

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from app.users.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app


def register_extensions(app):
    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)
    configure_uploads(app, photos)
    babel.init_app(app)
    cli.register(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
