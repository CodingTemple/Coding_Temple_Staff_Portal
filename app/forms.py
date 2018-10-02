from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role, Course, Instructor, Semester


class CourseForm(FlaskForm):
  name = StringField('Course')
  weeks = IntegerField("How many weeks is this course?", validators=[DataRequired()])
  start_date = DateField('Start date', validators=[DataRequired()])
  end_date = DateField('Start date', validators=[DataRequired()])