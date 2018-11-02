from app import login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String)
  l_name = db.Column(db.String)
  image = db.Column(db.String, default='http://placehold.it/400x900&text=Image')
  email = db.Column(db.String, index=True, unique=True)
  bio = db.Column(db.String, default = 'Enter a bio')
  password_hash = db.Column(db.String)

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

  def __repr__(self):
    return f"<Course: {self.name}>"

class Assignment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  due_date = db.Column(db.DateTime, index=True)
  date_submitted = db.Column(db.DateTime, index=True, default=datetime.utcnow())
  course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
  course = db.relationship('Course', backref='assignments', lazy='subquery')

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  note = db.Column(db.String)
  in_class = db.Column(db.Boolean)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User', backref='notes', lazy='subquery')

  def __repr__(self):
    return f"<Note: {self.date}, {self.note}, {self.in_class}>"

class UserRole(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    user = db.relationship('User', lazy='subquery', backref=db.backref('user_roles', lazy='dynamic'))
    role = db.relationship('Role', lazy='subquery', backref=db.backref('user_roles', lazy='dynamic'))

class UserCourse(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    completion_date = db.Column(db.DateTime)
    withdrawl_date = db.Column(db.DateTime)
    user = db.relationship('User', lazy='subquery', backref=db.backref('user_courses', lazy='dynamic'))
    course = db.relationship('Course', lazy='subquery', backref=db.backref('user_courses', lazy='dynamic'))

class UserAssignment(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), primary_key=True)
    completed_date = db.Column(db.DateTime)
    note = db.Column(db.String)
    user = db.relationship('User', lazy='subquery', backref=db.backref('user_assignments', lazy='dynamic'))
    assignment = db.relationship('Assignment', lazy='subquery', backref=db.backref('user_assignments', lazy='dynamic'))

@login.user_loader
def load_user(id):
  ''' Gets the user by their user ID'''
  return User.query.join(UserRole).join(Role).filter(User.id==int(id)).one()