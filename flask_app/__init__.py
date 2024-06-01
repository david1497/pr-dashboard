from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dash_app import create_dash_app
from flask_login import LoginManager

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

from flask_app import routes, models

if __name__ == '__main__':
    app.run(debug=True)
