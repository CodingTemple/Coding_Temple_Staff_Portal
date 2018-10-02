from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role


class CourseForm(FlaskForm):
  with app.app_context():
    name = StringField('Course')
    weeks = IntegerField("How many weeks is this course?", validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    submit = SubmitField('Add Course')
