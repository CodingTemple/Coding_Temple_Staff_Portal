from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.blueprints.roles.forms import RoleForm
from app.models import User, Role, db, Note

from app.decorators import authorize

roles = Blueprint('roles', __name__, template_folder='templates', static_folder='static')

@roles.route('/', methods=['GET'])
@login_required
@authorize
def index():
  context = {
    'roles': Role.query.all(),
    'title': 'Roles',
    'description': 'Manage Users and Roles'
  }
  return render_template('roles/index.html', **context)

@roles.route('/add', methods=['GET', 'POST'])
@login_required
@authorize
def add():
  form = RoleForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      role = Role(name= form.name.data)
      db.session.add(role)
      db.session.commit()
      flash('Role Added', 'Success')
      return redirect(url_for('.index'))
    else:
      flash('Choose a different role name', 'danger')
  context = {
    'form': form
  }
  return render_template('roles/add.html', **context)

@roles.route('/edit', methods=['GET', 'POST'])
@login_required
@authorize
def edit():
  form = RoleForm()
  rid = request.args.get('id') or form.rid.data
  role = Role.query.get(rid)
  if rid is None or role is None:
    flash('Role not found', 'danger')
    return redirect(url_for('.index'))
  if request.method == 'POST':
    if form.validate_on_submit():
      role.name = form.name.data
      db.session.commit()
      flash('Role updated', 'success')
      return redirect(url_for('.index'))
    else:
      flash('Choose a different role name', 'danger')
  form.name.data = role.name  
  form.rid.data = role.id
  context = {
    'form': form
  }
  return render_template('roles/edit.html', **context)

@roles.route('/delete', methods=['POST'])
@login_required
@authorize
def delete():
  rid = request.form['id']
  role =  Role.query.get(rid)
  role_name = role.name
  if role.users:
    flash('You cannot delete a role with users assigned to it', 'danger')
  else:
    db.session.delete(role)
    db.session.commit()
    flash('Deleted role ' + role_name, 'success')
  return redirect(url_for('.index'))
