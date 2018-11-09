from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField, HiddenField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Optional
from app.models import User, Course

class NoteForm(FlaskForm):
  date = DateField('Date', validators=[DataRequired()])
  time = TimeField('Time', validators=[Optional()])
  note = TextAreaField('Note', validators=[DataRequired()])
  absent = BooleanField('absent')
  user = SelectField('User', validators=[DataRequired()], coerce=int)
  submit = SubmitField('Save')

  def __init__(self):
    super().__init__()
    self.user.choices = [(-1, "")]+[(i.id, i.f_name + " " + i.l_name) for i in User.query.all()]