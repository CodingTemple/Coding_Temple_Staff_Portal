from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, HiddenField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role, Note, Course, Semester, Instructor


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


class CourseForm(FlaskForm):
  with app.app_context():
    name = StringField('Course')
    weeks = IntegerField("How many weeks is this course?", validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    semester = SelectField('Pick a semester', validators=[DataRequired()], choices=[(i.id, i.name) for i in Semester.query.all()], coerce=int)
    instructor = SelectField("Who's the instructor", validators=[DataRequired()], choices=[(i.id, i.f_name) for i in Instructor.query.all()], coerce=int)
    submit = SubmitField('Add Course')
