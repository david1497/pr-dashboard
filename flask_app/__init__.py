from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dash_app import create_dash_app
from flask_login import LoginManager
import logging, os
from logging.handlers import RotatingFileHandler, SMTPHandler

server = 'laptop-ttip97em\\sqlexpress'
database = 'platt_reilly'
driver = 'ODBC+Driver+17+for+SQL+Server'

app = Flask(__name__)
app.config['DEBUG'] = 1
app.config['SECRET_KEY'] = 'you-will-never-guess'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://@{server}/{database}?driver={driver};Trusted_Connection=yes;'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://@{server}/{database}?driver={driver}&Trusted_Connection=yes'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
migrate = Migrate(app, db)


# Function to create and register the first Dash app
create_dash_app(app)

from flask_app import routes, models, errors

if not app.debug:

    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='PlattReilly Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/platt_reilly.log', 
                                       maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('PlatReilly startup')


if __name__ == '__main__':
    app.run(debug=True)
