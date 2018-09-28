from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import Semester, Instructor


class CourseForm(FlaskForm):
  with app.app_context():
    name = StringField('Course')
    weeks = IntegerField("How many weeks is this course?", validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    semester = SelectField('Pick a semester', validators=[DataRequired()], choices=[(i.id, i.name) for i in Semester.query.all()], coerce=int)
    instructor = SelectField("Who's the instructor", validators=[DataRequired()], choices=[(i.id, i.f_name) for i in Instructor.query.all()], coerce=int)
    submit = SubmitField('Add Course')
