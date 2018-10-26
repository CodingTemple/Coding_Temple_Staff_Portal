from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import app
from app.models import User, Role


class CourseForm(FlaskForm):
  with app.app_context():
    cid = HiddenField('ID')
    name = StringField('Course')
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    submit = SubmitField('Save')
