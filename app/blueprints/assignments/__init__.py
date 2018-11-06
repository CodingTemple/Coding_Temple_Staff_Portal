from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.models import db, Assignment, Course

from app.blueprints.assignments.forms import AssignmentForm
from app.decorators import authorize

assignments = Blueprint('assignments', __name__, template_folder='templates', static_folder='static')

@assignments.route('/edit', methods=['GET', 'POST'])
@login_required
@authorize
def edit():
  id = request.form['id']
  context = {
    
  }
  return render_template('assignments/edit.html', **context)

@assignments.route('/', methods=['GET'])
@login_required
@authorize
def index():
  course_id = request.args.get('cid')
  courses = Course.query.all()
  if(course_id):
    assignments = Assignment.query.filter_by(course_id=course_id).all()
  else:
    assignments = Assignment.query.all()
  context = {
      'courses': courses,
      'assignments': assignments,
      'title': 'Assignments',
      'course_id': int(course_id or 0)
  }
  return render_template('assignments/index.html', **context)

@assignments.route('/add', methods=['GET', 'POST'])
@login_required
@authorize
def add():
  form = AssignmentForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      assignment = Assignment(name=form.name.data, due_date=form.due_date.data, description=form.description.data, course_id=form.course.data)
      db.session.add(assignment)
      db.session.commit()
      flash('Assignment Added', 'success')
      return redirect(url_for('assignments.index'))
    else:
      print(form.errors)
      flash('Assignment is invalid', 'danger')
  context = {
      'form': form
  }
  return render_template('assignments/add.html', **context)

@assignments.route('/delete', methods=['POST'])
@login_required
@authorize
def delete():
  id = request.form['id']
  return redirect(url_for('assigments.index'))