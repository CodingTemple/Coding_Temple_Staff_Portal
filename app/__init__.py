from flask import Flask
app = Flask(__name__)
from config import Config
app.config.from_object(Config)

from flask_login import LoginManager
login = LoginManager()
login.init_app(app)

from flask_moment import Moment
moment = Moment(app)

from app.models import db
db.init_app(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)

from app.blueprints.users import users
app.register_blueprint(users,  url_prefix='/users')

from app.blueprints.roles import roles
app.register_blueprint(roles,  url_prefix='/roles')

from app.blueprints.account import account
app.register_blueprint(account, url_prefix='/account')

from app.blueprints.courses import courses
app.register_blueprint(courses, url_prefix='/courses')

from app.blueprints.notes import notes
app.register_blueprint(notes, url_prefix='/notes')

from app.blueprints.assignments import assignments
app.register_blueprint(assignments, url_prefix='/assignments')

from app import routes, models, errors