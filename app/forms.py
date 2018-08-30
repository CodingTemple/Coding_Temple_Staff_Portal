from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import User, Role

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


class AdminForm(FlaskForm):
  f_name = StringField('First Name', validators=[DataRequired()])
  l_name = StringField('Last Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  role = SelectField('Role', validators=[DataRequired()], choices=[(i.id, i.name) if i else (i.id, i.name) for i in Role.query.order_by('name').all()], coerce=int)
  submit = SubmitField('Create User')

  def validate_email(self, email):
    u = User.query.filter_by(email=email.data).first()
    if u is not None:
      raise ValidationError('Please use a different email.')
