from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, TextAreaField, FileField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role, db

class RegistrationForm(FlaskForm):
  f_name = StringField('First Name', validators=[DataRequired()])
  l_name = StringField('Last Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_email(self, email):
    u = User.query.filter_by(email=email.data).first()
    if u is not None:
      raise ValidationError('Please use a different email.')


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me', description='Remember Me')
  submit = SubmitField('Login')


class ProfileForm(FlaskForm):
  image = FileField('Image')
  first_name = StringField('First Name', description='First Name', validators=[DataRequired()])
  last_name = StringField('Last Name', description='Last Name', validators=[DataRequired()])
  email = StringField('Email', description='Email', validators=[Email(), DataRequired()])
  bio = TextAreaField('Bio', description='Write a short bio...')
  submit = SubmitField('Submit')
