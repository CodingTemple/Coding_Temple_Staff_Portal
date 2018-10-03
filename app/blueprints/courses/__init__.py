from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.blueprints.courses.forms import CourseForm
from app.models import Course

from app.decorators import authorize

courses = Blueprint('courses', __name__, template_folder='templates', static_folder='static')

@courses.route('/details', methods=['GET', 'POST'])
@login_required
@authorize
def details():
  form = CourseForm()
  if form.validate_on_submit():
    course = Course()
    db.session.add(course)
    db.session.commit()
    flash('Course added')
    return redirect(url_for('index'))


  context = {
    'form': form,
    'title': 'Course',
    'notes': Note.query.order_by('date DESC').all()
  }
  return render_template('courses/details.html', **context)


@courses.route('/', methods=['GET'])
@login_required
@authorize
def index():
  form = CourseForm()
  context = {
      'form': form,
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
      course = Course(name=form.name.data, start_date=form.start_date.data, end_date=form.end_date.data, weeks=form.weeks.data, instructor_id=form.instructor.data, semester_id=form.semester.data)
      db.session.add(course)
      db.session.commit()
      flash('Course Added', 'Success')
      return redirect(url_for('index'))
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
    flash('Deleted course ' + course.name, 'success', 'success')
  else:
    flash('Cannot delete this course', 'danger')
  return redirect(url_for('/index'))
