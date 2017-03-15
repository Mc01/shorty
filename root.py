from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

from app.controller import Controller

app = Flask(
    __name__, template_folder='templates'
)
app.config.from_pyfile('app/config/.env')
admin = Admin(app, name='shorty', template_mode='bootstrap3')
db = SQLAlchemy(app)
controller = Controller()
