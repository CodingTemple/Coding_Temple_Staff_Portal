import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
  SECRET_KEY = os.urandom(24)
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SUPER_USER_PASSWORDS = [os.getenv('SU_1')]
  PROFILE_PICS_FOLDER = os.path.join(basedir, 'app/blueprints/account/static/uploads')
