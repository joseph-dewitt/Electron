from config import Config
from flask import Flask
from flask import request
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
import os
import sass

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment(app)

from app import routes, models, errors

if app.config['MAIL_SERVER']:
	auth = None
	if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
		auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
	secure = None
	if app.config['MAIL_USE_TLS']:
		secure = ()
	mail_handler = SMTPHandler(
		mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
		fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
		toaddrs = app.config['ADMINS'],
		subject = 'Joe dun borked up',
		credentials = auth,
		secure = secure
		)
if not app.debug:
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler(
		'logs/electron.log',
		maxBytes = 10240,
		backupCount = 10)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
		))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)

	app.logger.setLevel(logging.INFO)
	app.logger.info('Electron has started')

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
