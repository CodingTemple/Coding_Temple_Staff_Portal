from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.models import db, Assignment

from app.decorators import authorize

assignments = Blueprint('assignments', __name__, template_folder='templates', static_folder='static')

@assignments.route('/edit', methods=['GET', 'POST'])
@login_required
@authorize
def edit():
  context = {
    
  }
  return render_template('assignments/edit.html', **context)

@assignments.route('/', methods=['GET'])
@login_required
@authorize
def index():
  context = {
      'assignments': Assignment.query.all(),
      'title': 'Assignments'
  }
  return render_template('assignments/index.html', **context)

@assignments.route('/add', methods=['GET', 'POST'])
@login_required
@authorize
def add():
  context = {
  }
  return render_template('assignments/add.html', **context)

@assignments.route('/delete', methods=['POST'])
@login_required
@authorize
def delete():
  return redirect(url_for('assigments.index'))