from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String)
  l_name = db.Column(db.String)
  image = db.Column(db.String, default='http://placehold.it/400x900&text=Image')
  email = db.Column(db.String, index=True, unique=True)
  password_hash = db.Column(db.String)
  role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
  role = db.relationship('Role', backref='role')

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return f"<User: {self.f_name} {self.l_name}, {self.email}>"


class Role(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  users = db.relationship('User', backref='user', lazy='dynamic')

  def __repr__(self):
    return f"<Role: {self.name}>"


class Instructor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  course_id = db.Column(db.Integer, db.ForeignKey('course.id'))


class Course(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)
  weeks = db.Column(db.Integer)
  students = db.relationship('Student', backref='course', lazy='dynamic')
  semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
  instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))

  def __repr__(self):
    return f"<Course: {self.name}>"


class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
  days_missed = db.Column(db.Integer)
  assignments = db.relationship('Assignment', backref='assignment', lazy='dynamic')


class Semester(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  courses = db.relationship('Course', backref='course', lazy='dynamic')


class Assignment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  due_date = db.Column(db.DateTime, index=True)
  date_submitted = db.Column(db.DateTime, index=True, default=datetime.utcnow())
  student_id = db.Column(db.Integer, db.ForeignKey('student.id'))


@login.user_loader
def load_user(id):
  return User.query.get(int(id))