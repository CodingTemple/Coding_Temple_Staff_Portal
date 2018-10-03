from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, HiddenField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role, Note, Course

class RoleForm(FlaskForm):
  rid = HiddenField('ID')
  name = StringField('Name', validators=[DataRequired()])
  submit = SubmitField('Save')
  def validate_name(self, name):
    local_id = self.rid.data
    local_name = self.name.data
    # r = Role.query.filter(Role.name==local_name).filter(Role.id!=local_id).first()
    r = Role.query.filter(Role.name==local_name).first()
    if r is not None:
      raise ValidationError('Please use a different name')

