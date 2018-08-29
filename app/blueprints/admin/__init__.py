from flask import abort, Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app.blueprints.admin.forms import AdminForm, RoleForm
from app.models import User, Role, db

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@login_required
@admin.route('/', methods=['GET'])
def index():
  if not current_user.is_authenticated or not current_user.role.name == 'Super User':
    abort(401)
  context = {
    'title': 'User Administration',
    'description': 'Manage Users and Roles'
  }
  return render_template('admin/index.html', **context)

@login_required
@admin.route('/roles', methods=['GET'])
def roles():
  if not current_user.is_authenticated or not current_user.role.name == 'Super User':
    abort(401)
  context = {
    'roles': Role.query.all(),
    'title': 'Roles',
    'description': 'Manage Users and Roles'
  }
  return render_template('admin/roles.html', **context)

@login_required
@admin.route('/roles/add', methods=['GET'])
def rolesadd():
  if not current_user.is_authenticated or not current_user.role.name == 'Super User':
    abort(401)
  form = RoleForm()
  context = {
    'form': form
  }
  return render_template('admin/rolesadd.html', **context)

@login_required
@admin.route('/roles/edit', methods=['GET'])
def rolesedit():
  if not current_user.is_authenticated or not current_user.role.name == 'Super User':
    abort(401)
  context = {
    
  }
  return render_template('admin/rolesedit.html', **context)

@login_required
@admin.route('/roles/delete', methods=['GET'])
def rolesdelete():
  if not current_user.is_authenticated or not current_user.role.name == 'Super User':
    abort(401)
  flash('You called delete', 'warning')
  return redirect(url_for('admin.roles'))

@login_required
@admin.route('/users', methods=['GET', 'POST'])
def users():
  if not current_user.is_authenticated or not current_user.role.name == 'Super User':
    abort(401)
  form = AdminForm()
  if form.validate_on_submit():
    print(form.role.data)
    print("begin validation...")
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None:
      flash('That email is already taken. Choose another.', 'danger')
      return redirect(url_for('.index'))
    new_user = User(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, role_id=form.role.data)
    new_user.set_password(form.email.data)
    db.session.add(new_user)
    db.session.commit()
    flash('New user created.', 'success')
    return redirect(url_for('.index'))
  context = {
    'form': AdminForm(),
    'description': 'Create a new user',
    'title': 'Admin'
  }
  return render_template('admin/users.html', **context)