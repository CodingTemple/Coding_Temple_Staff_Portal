from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, HiddenField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

class NoteForm(FlaskForm):
  date = DateField('Date', validators=[DataRequired()])
  time = TimeField('Time', validators=[DataRequired()])
  note = StringField('Note', validators=[DataRequired()])
  in_class = BooleanField('Cancel')
  submitnote = SubmitField('Submit Note')
