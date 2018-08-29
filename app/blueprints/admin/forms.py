from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role


class AdminForm(FlaskForm):
  with app.app_context():
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', validators=[DataRequired()], choices=[(i.id, i.name) for i in Role.query.all()], coerce=int)
    # role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Create User')

  def validate_email(self, email):
    u = User.query.filter_by(email=email.data).first()
    if u is not None:
      raise ValidationError('Please use a different email.')

class RoleForm(FlaskForm):
  id = HiddenField('ID')
  name = StringField('Name', validators=[DataRequired()])
  submit = SubmitField('Submit')
  def validate_name(self, name):
    r = Role.query.filter_by(name=name.data).first()
    if r is not None:
      raise ValidationError('Please use a different name')