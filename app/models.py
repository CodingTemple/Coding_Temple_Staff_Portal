
from app import login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


userRole = db.Table('userrole',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

userCourse = db.Table('usercourse',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('completion_date',db.DateTime),
    db.Column('withdrawl_date',db.DateTime),
)

userAssignment = db.Table('userassignment',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignment.id'), primary_key=True),
    db.Column('completed_date', db.DateTime),
    db.Column('note', db.String)
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String)
  l_name = db.Column(db.String)
  image = db.Column(db.String, default='http://placehold.it/400x900&text=Image')
  email = db.Column(db.String, index=True, unique=True)
  bio = db.Column(db.String, default = 'Enter a bio')
  password_hash = db.Column(db.String)
  roles = db.relationship('Role', secondary=userRole, lazy='dynamic', backref=db.backref('users', lazy='dynamic'))
  courses = db.relationship('Course', secondary=userCourse, lazy='dynamic', backref=db.backref('users', lazy='dynamic'))
  assignments = db.relationship('Assignment', secondary=userAssignment, lazy='dynamic', backref=db.backref('users', lazy='dynamic'))
  notes = db.relationship('Note', backref='users', lazy='dynamic')

  def set_password(self, password):
    '''Sets the password_hash property via a built-in hash function'''
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    '''Checks the password against the saved, hashed password value'''
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return f"<User: {self.f_name} {self.l_name}, {self.email}>"

class Role(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)

  def __repr__(self):
    return f"<Role: {self.name}>"

class Course(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)
  assignments = db.relationship('Assignment', backref='course', lazy='dynamic')

  def __repr__(self):
    return f"<Course: {self.name}>"

class Assignment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  due_date = db.Column(db.DateTime, index=True)
  date_submitted = db.Column(db.DateTime, index=True, default=datetime.utcnow())
  course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  note = db.Column(db.String)
  in_class = db.Column(db.Boolean)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f"<Note: {self.date}, {self.note}, {self.in_class}>"

@login.user_loader
def load_user(id):
  ''' Gets the user by their user ID'''
  return User.query.get(int(id))