from app import login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

userRole = db.Table('user_role', 
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(UserMixin, TimestampMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String)
  preferred_name = db.Column(db.String)
  l_name = db.Column(db.String)
  image = db.Column(db.String, default='http://placehold.it/400x900&text=Image')
  email = db.Column(db.String, index=True, unique=True)
  bio = db.Column(db.String, default = 'Enter a bio')
  password_hash = db.Column(db.String)
  roles = db.relationship('Role', secondary=userRole, lazy='subquery', backref=db.backref('users', lazy=True))
  contact_phone = db.Column(db.String, nullable=True)
  personal_website = db.Column(db.String, nullable=True)
  street_address = db.Column(db.String, nullable=True)
  city = db.Column(db.String, nullable=True)
  state = db.Column(db.String, nullable=True)
  postal_code = db.Column(db.String, nullable=True)
  linkedin_url = db.Column(db.String, nullable=True)
  github_name = db.Column(db.String, nullable=True)
  twitter_name = db.Column(db.String, nullable=True)
  employment_histories = db.relationship('EmploymentHistory', backref='user', lazy=True)
  
  def set_password(self, password):
    '''Sets the password_hash property via a built-in hash function'''
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    '''Checks the password against the saved, hashed password value'''
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return f"<User: {self.f_name} {self.l_name}, {self.email}>"

class EmploymentHistory(TimestampMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  title = db.Column(db.String, nullable=False)
  salary = db.Column(db.Numeric, nullable=True)
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)

class Role(TimestampMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)

  def __repr__(self):
    return f"<Role: {self.name}>"

class Course(TimestampMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)

  def __repr__(self):
    return f"<Course: {self.name}>"

class Assignment(TimestampMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  due_date = db.Column(db.DateTime, index=True)
  date_submitted = db.Column(db.DateTime, index=True, default=datetime.utcnow())
  course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
  course = db.relationship('Course', backref='assignments', lazy='subquery')

class Note(TimestampMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  note = db.Column(db.String)
  absent = db.Column(db.Boolean)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User', backref='notes', lazy='subquery')

  def __repr__(self):
    return f"<Note: {self.date}, {self.note}, {self.absent}>"

class UserCourse(TimestampMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    completion_date = db.Column(db.DateTime, nullable=True)
    withdrawl_date = db.Column(db.DateTime, nullable=True)
    withdrawl_reason = db.Column(db.String, nullable=True)
    user = db.relationship('User', lazy='subquery', backref=db.backref('user_courses', lazy='dynamic'))
    course = db.relationship('Course', lazy='subquery', backref=db.backref('user_courses', lazy='dynamic'))

class UserAssignment(TimestampMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), primary_key=True)
    completed_date = db.Column(db.DateTime, nullable=True)
    note = db.Column(db.String, nullable=True)
    user = db.relationship('User', lazy='subquery', backref=db.backref('user_assignments', lazy='dynamic'))
    assignment = db.relationship('Assignment', lazy='subquery', backref=db.backref('user_assignments', lazy='dynamic'))

@login.user_loader
def load_user(id):
  ''' Gets the user by their user ID'''
  return User.query.get(int(id))