from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.blueprints.courses.forms import CourseForm
from app.models import db, Course, UserCourse

from app.decorators import authorize

import re
import datetime

courses = Blueprint('courses', __name__, template_folder='templates', static_folder='static')

@courses.route('/edit', methods=['GET', 'POST'])
@login_required
@authorize
def edit():
  form = CourseForm()
  cid = request.args.get('id') or form.cid.data
  course = Course.query.get(cid)
  if cid is None or course is None:
    flash('Course not found', 'danger')
    return redirect(url_for('courses.index'))
  if request.method == 'POST':
    if form.validate_on_submit():
      course.start_date = form.start_date.data
      course.end_date = form.end_date.data
      course.name = form.name.data
      db.session.commit()
      flash('Course updated', 'success')
      return redirect(url_for('courses.index'))
    else:
      flash('Could not update course', 'danger')
  form.name.data = course.name
  form.start_date.data = course.start_date
  form.end_date.data = course.end_date  
  form.cid.data = course.id
  context = {
    'form': form
  }
  return render_template('courses/edit.html', **context)


@courses.route('/', methods=['GET'])
@login_required
@authorize
def index():
  context = {
      'courses': Course.query.order_by('start_date').all(),
      'title': 'Courses'
  }
  return render_template('courses/index.html', **context)


@courses.route('/add', methods=['GET', 'POST'])
@login_required
@authorize
def add():
  form = CourseForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      course = Course(name=form.name.data, start_date=form.start_date.data, end_date=form.end_date.data)
      db.session.add(course)
      db.session.commit()
      flash('Course Added', 'success')
      return redirect(url_for('courses.index'))
    else:
      flash('Choose a different role name', 'danger')
  context = {
      'form': form
  }
  return render_template('courses/add.html', **context)

@courses.route('/delete', methods=['POST'])
@login_required
@authorize
def delete():
  co_id = request.form['id']
  course = Course.query.get(co_id)
  if course is not None:
    db.session.delete(course)
    db.session.commit()
    flash('Deleted course ' + course.name, 'success')
  else:
    flash('Cannot delete this course', 'danger')
  return redirect(url_for('courses.index'))

@courses.route('/usercourses', methods=['GET', 'POST'])
@login_required
@authorize
def usercourses():
  id = request.args.get('id')
  course = Course.query.get(id)
  if request.method == 'POST':
    posted_user_courses = []
    for key in request.form.keys():
      if(key.startswith('user_course')):
        trimmed_key = key[11:] 
        id = int(re.search('\[(.*?)\]', trimmed_key).group(1))
        prop =  trimmed_key[trimmed_key.index('.')+1:]
        if(len(posted_user_courses) == id):
          posted_user_courses.insert(id,{})
        posted_user_courses[id][prop] = request.form.getlist(key)[0]
    for posted_user_course in posted_user_courses:
      existing_user_course = UserCourse.query.get([posted_user_course['user_id'], posted_user_course['course_id']])
      if existing_user_course.withdrawl_date != posted_user_course['withdrawl_date']:
        if posted_user_course['withdrawl_date'] != '':
          existing_user_course.withdrawl_date = datetime.datetime.strptime(posted_user_course['withdrawl_date'], '%Y-%m-%d')
        else:
          existing_user_course.withdrawl_date = None
      if existing_user_course.withdrawl_reason != posted_user_course['withdrawl_reason']:
        existing_user_course.withdrawl_reason = posted_user_course['withdrawl_reason']
      
      db.session.commit()
    return redirect(url_for('courses.usercourses') + "?id=" + str(course.id))
  else:
    user_courses = course.user_courses.all()
  print(user_courses)
  context = {
      'course': course,
      'user_courses': user_courses
  }
  return render_template('courses/usercourses.html', **context)

@courses.route('/useradd', methods=['POST'])
@login_required
@authorize
def useradd():
  uid = request.json['uid']
  cid = request.json['cid']
  newUserCourse = UserCourse(user_id=uid, course_id=cid)
  db.session.add(newUserCourse)
  db.session.commit()
  return redirect(url_for('courses.usercourses') + "?id=" + cid)

@courses.route('/userdelete', methods=['POST'])
@login_required
@authorize
def userdelete():
  uid = request.json['uid']
  cid = request.json['cid']
  course = UserCourse.query.get([uid, cid])
  db.session.delete(course)
  db.session.commit()
  return redirect(url_for('courses.usercourses') + "?id=" + cid)


