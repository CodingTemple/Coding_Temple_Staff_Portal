from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.blueprints.admin.forms import AdminForm, RoleForm, NoteForm
from app.models import User, Role, db, Note

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@login_required
@admin.route('/', methods=['GET'])
def index():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all() :
    abort(401)
  context = {
    'title': 'User Administration',
    'description': 'Manage Users and Roles'
  }
  return render_template('admin/index.html', **context)

@login_required
@admin.route('/roles', methods=['GET'])
def roles():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  context = {
    'roles': Role.query.all(),
    'title': 'Roles',
    'description': 'Manage Users and Roles'
  }
  return render_template('admin/roles.html', **context)

@login_required
@admin.route('/roles/add', methods=['GET', 'POST'])
def rolesadd():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  form = RoleForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      role = Role(name= form.name.data)
      db.session.add(role)
      db.session.commit()
      flash('Role Added', 'Success')
      return redirect(url_for('.roles'))
    else:
      flash('Choose a different role name', 'danger')
  context = {
    'form': form
  }
  return render_template('admin/rolesadd.html', **context)

@login_required
@admin.route('/roles/edit', methods=['GET', 'POST'])
def rolesedit():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  form = RoleForm()
  rid = request.args.get('id') or form.rid.data
  role = Role.query.filter_by(id=rid).first()
  if rid is None or role is None:
    flash('Role not found', 'danger')
    return redirect(url_for('.roles'))
  if request.method == 'POST':
    if form.validate_on_submit():
      role.name = form.name.data
      db.session.commit()
      flash('Role updated', 'success')
      return redirect(url_for('.roles'))
    else:
      flash('Choose a different role name', 'danger')
  form.name.data = role.name  
  form.rid.data = role.id
  context = {
    'form': form
  }
  return render_template('admin/rolesedit.html', **context)

@login_required
@admin.route('/roles/delete', methods=['POST'])
def rolesdelete():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  rid = request.form['id']
  userCount = User.query.filter(User.role_id == rid).count()
  if userCount > 0:
    flash('You cannot delete a role with users assigned to it', 'danger')
  else:
    role = Role.query.filter(Role.id == rid).first()
    role_name = role.name
    db.session.delete(role)
    db.session.commit()
    flash('Deleted role ' + role_name, 'success')
  return redirect(url_for('.roles'))

@login_required
@admin.route('/users', methods=['GET'])
def users():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  rid = request.args.get('role')
  if rid is not None:
    users = User.query.filter(User.role_id == rid).all()
  else:
    users = User.query.all()
  context = {
    'users': users
  }
  return render_template('admin/users.html', **context)

@login_required
@admin.route('/users/edit', methods=['GET', 'POST'])
def usersedit():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  form = AdminForm()
  uid = request.args.get('id') or request.form['uid'] 
  cuid = current_user.id
  user = User.query.filter(User.id == uid).filter(User.id != cuid).first()
  if request.method == 'POST':
    if form.validate_on_submit():
      if user is not None:
        user.f_name = form.f_name.data
        user.l_name = form.l_name.data
        user.role_id = form.role.data
        db.session.commit()
        flash('Updated user ' + uid, 'success') 
        return redirect(url_for('.users'))
    flash('Could not update user.', 'danger')
  form.f_name.data = user.f_name
  form.l_name.data = user.l_name
  form.role.data = user.role_id
  form.email.data = user.email
  context = {
    'id': user.id,
    'email': user.email,
    'form': form,
    'description': 'Update user',
    'title': 'Admin'
  }
  return render_template('admin/usersedit.html', **context)

@login_required
@admin.route('/users/delete', methods=['POST'])
def usersdelete():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  uid = request.form['id']
  cuid = current_user.id
  user = User.query.filter(User.id == uid).filter(User.id != cuid).first()
  if user is not None:
    db.session.delete(user)
    db.session.commit()
    flash('Deleted user ' + uid, 'success')
  else:
    flash('Cannot delete this user', 'danger')
  return redirect(url_for('.users'))
  

@login_required
@admin.route('/users/add', methods=['GET', 'POST'])
def usersadd():
  if not current_user.is_authenticated or not current_user.roles.filter_by(name = "Super User").all():
    abort(401)
  form = AdminForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      new_user = User(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, role_id=form.role.data)
      new_user.set_password(form.email.data)
      db.session.add(new_user)
      db.session.commit()
      if new_user.role_id==3:
        new_student = Student(f_name=new_user.f_name, l_name=new_user.l_name, user_id=User.query.filter(User.email == new_user.email).first().id)
        db.session.add(new_student)
        db.session.commit()
      if new_user.role_id==4:
        new_instructor = Instructor(f_name=new_user.f_name, l_name=new_user.l_name, user_id=User.query.filter(User.email == new_user.email).first().id)
        db.session.add(new_instructor)
        db.session.commit()
      flash('New user created.', 'success')
      return redirect(url_for('.users'))
    else:
      flash('That email is already taken. Choose another.', 'danger')
      return redirect(url_for('.usersadd'))
  else:
    context = {
      'form': AdminForm(),
      'description': 'Create a new user',
      'title': 'Admin'
    }
    return render_template('admin/usersadd.html', **context)