from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField, HiddenField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import User, Course

class NoteForm(FlaskForm):
  date = DateField('Date', validators=[DataRequired()])
  time = TimeField('Time', validators=[DataRequired()])
  note = TextAreaField('Note', validators=[DataRequired()])
  in_class = BooleanField('In Class')
  user = SelectField('User', validators=[DataRequired()])
  course = SelectField('Course', validators=[DataRequired()])
  submitnote = SubmitField('Submit Note')

  def __init__(self):
    super().__init__()
    self.user.choices = [("", "")]+[(i.id, i.f_name + " " + i.l_name) for i in User.query.all()]
    self.course.choices = [("", "")]+[(i.id, i.name) for i in Course.query.all()]