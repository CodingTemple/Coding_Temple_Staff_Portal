from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app import app
from app.models import Course


class AssignmentForm(FlaskForm):
  with app.app_context():
    id = HiddenField('ID')
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    course = SelectField('Course', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Save')

    def __init__(self):
        super().__init__()
        self.course.choices = [("-1", "")]+[(i.id, i.name) for i in Course.query.all()]

class UserAssignmentForm(FlaskForm):
  with app.app_context():
    id = HiddenField('ID')
    completed_date = DateField('Completed Date')
    note = TextAreaField('Note')
  