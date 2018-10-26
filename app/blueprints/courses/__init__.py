from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.blueprints.courses.forms import CourseForm
from app.models import db, Course

from app.decorators import authorize

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
