from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role, Course, Instructor, Semester

class ProfileForm(FlaskForm):
  image = StringField('Upload an image')
  # class_ = SelectField('Class', validators=[DataRequired()], choices=[(i.id, i.name) if i else (i.id, i.name) for i in Course.query.all()], coerce=int)
  # semester = SelectField('Semester', validators=[DataRequired()], choices=[(i.id, i.name) for i in Semester.query.all()])
  # instructor = SelectField('Instructor', validators=[DataRequired()], choices=[(i.id, i.name) for i in Instructor.query.all()], coerce=int)
  submit = SubmitField('Submit')


class CourseForm(FlaskForm):
  name = StringField('Course')
  weeks = IntegerField("How many weeks is this course?", validators=[DataRequired()])
  start_date = DateField('Start date', validators=[DataRequired()])
  end_date = DateField('Start date', validators=[DataRequired()])
  semester = SelectField('Pick a semester', validators=[DataRequired()])
  instructor = SelectField("Who's the instructor", validators=[DataRequired()])