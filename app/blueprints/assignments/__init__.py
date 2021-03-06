from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for, jsonify
from flask_login import current_user, login_required
from app.models import db, Assignment, Course, UserAssignment, UserCourse

from app.blueprints.assignments.forms import AssignmentForm
from app.decorators import authorize

import datetime

assignments = Blueprint('assignments', __name__, template_folder='templates', static_folder='static')

@assignments.route('/edit', methods=['GET', 'POST'])
@login_required
@authorize
def edit():
  id = request.args.get('id') or request.form['id']
  assignment = Assignment.query.get(id)
  form = AssignmentForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      assignment.course_id = form.course.data 
      assignment.description = form.description.data
      assignment.due_date = form.due_date.data
      assignment.name = form.name.data
      db.session.commit()
      flash('Assignment updated', 'success')
      return redirect(url_for('assignments.index'))
    else:
      print(form.errors)
      flash('Assignment is invalid', 'danger')
  else:
    form.course.data = assignment.course_id
    form.description.data = assignment.description
    form.due_date.data = assignment.due_date
    form.id.data = assignment.id
    form.name.data = assignment.name
  context = {
      'form': form
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
  assignment = Assignment.query.get(id)
  assignment_name = assignment.name
  if(assignment.user_assignments.count() > 0):
    flash('You cannot an assignment that is assigned to users', 'danger')
  else:
    db.session.delete(assignment)
    db.session.commit()
    flash('Deleted assignment ' + assignment_name, 'success')
  return redirect(url_for('assignments.index'))


@assignments.route('/userassignments', methods=['GET'])
@login_required
@authorize
def userassignments():
  id = int(request.args.get('id'))
  assignment = Assignment.query.get(id)
  # Add all existing assignments:
  for user_course in assignment.course.user_courses:
    emptyAssignment = next((obj for obj in assignment.user_assignments if obj.user_id==user_course.user_id), None)
    if emptyAssignment is None:
      emptyAssignment = UserAssignment(assignment_id = id, user_id=user_course.user_id)
      db.session.add(emptyAssignment)
      db.session.commit()
  context = {
      'assignment': assignment,
  }
  return render_template('assignments/userassignments.html', **context)

@assignments.route('/userupdate', methods=['POST'])
@login_required
@authorize
def userupdate():
  assignment_id = int(request.json['aid'])
  user_id = int(request.json['uid'])
  completed_date = request.json['cd']
  note = request.json['n']
  userAssignment = UserAssignment.query.get([user_id, assignment_id])
  userAssignment.note = note
  if(completed_date):
    userAssignment.completed_date = datetime.datetime.strptime(completed_date,'%Y-%m-%d')
  db.session.commit()
  return jsonify(success=True)