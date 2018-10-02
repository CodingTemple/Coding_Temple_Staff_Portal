from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, HiddenField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role, Note, Course


class AdminForm(FlaskForm):
  with app.app_context():
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Create User')

  def validate_email(self, email):
    u = User.query.filter_by(email=email.data).first()
    if u is not None:
      raise ValidationError('Please use a different email.')
  
  def __init__(self):
    super(app, self).__init__()
    self.role.choices = [(i.id, i.name) for i in Role.query.all()]

class RoleForm(FlaskForm):
  rid = HiddenField('ID')
  name = StringField('Name', validators=[DataRequired()])
  submit = SubmitField('Submit')
  def validate_name(self, name):
    local_id = self.rid.data
    local_name = self.name.data
    # r = Role.query.filter(Role.name==local_name).filter(Role.id!=local_id).first()
    r = Role.query.filter(Role.name==local_name).first()
    if r is not None:
      raise ValidationError('Please use a different name')

class NoteForm(FlaskForm):
  date = DateField('Date', validators=[DataRequired()])
  time = TimeField('Time', validators=[DataRequired()])
  note = StringField('Note', validators=[DataRequired()])
  in_class = BooleanField('Cancel')
  submitnote = SubmitField('Submit Note')

