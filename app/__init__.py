from flask import Flask
app = Flask(__name__)
from config import Config
app.config.from_object(Config)

from flask_login import LoginManager
login = LoginManager()
login.init_app(app)

from app.models import db
db.init_app(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)

from app.blueprints.admin import admin
app.register_blueprint(admin,  url_prefix='/admin')
from app.blueprints.account import account

app.register_blueprint(account)
from app import routes, models, errors


