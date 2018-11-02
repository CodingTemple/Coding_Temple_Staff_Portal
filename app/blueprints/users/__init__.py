from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.blueprints.users.forms import UserForm
from app.models import User, Role, db, Note, UserRole

from app.decorators import authorize

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')

@users.route('/', methods=['GET'])
@login_required
@authorize
def index():
  rid = request.args.get('role')
  if rid is not None:
    users = list(map(lambda x: x.user, Role.query.get(rid).user_roles.all()))
  else:
    users = User.query.all()
  context = {
    'users': users
  }
  return render_template('users/index.html', **context)

@users.route('/edit', methods=['GET', 'POST'])
@login_required
@authorize
def edit():
  form = UserForm()
  uid = request.args.get('id') or request.form['uid'] 
  cuid = current_user.id
  user = User.query.filter(User.id == uid).filter(User.id != cuid).first()
  if request.method == 'POST':
    if form.validate_on_submit():
      if user is not None:
        user.f_name = form.f_name.data
        user.l_name = form.l_name.data
        user.user_roles.append(UserRole(role_id=form.role.data))
        db.session.commit()
        flash('Updated user ' + uid, 'success') 
        return redirect(url_for('.index'))
    flash('Could not update user.', 'danger')
  form.f_name.data = user.f_name
  form.l_name.data = user.l_name
  user_role = user.user_roles.first().role
  if(user_role) :
    form.role.data = user_role
  form.email.data = user.email
  context = {
    'id': user.id,
    'email': user.email,
    'form': form,
    'description': 'Update user',
    'title': 'Admin'
  }
  return render_template('users/edit.html', **context)

@users.route('/delete', methods=['POST'])
@login_required
@authorize
def delete():
  uid = request.form['id']
  cuid = current_user.id
  user = User.query.filter(User.id == uid).filter(User.id != cuid).first()
  if user is not None:
    db.session.delete(user)
    db.session.commit()
    flash('Deleted user ' + uid, 'success')
  else:
    flash('Cannot delete this user', 'danger')
  return redirect(url_for('.index'))
  
@users.route('/add', methods=['GET', 'POST'])
@login_required
@authorize
def add():
  form = UserForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      new_user = User(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data)
      new_user_role = UserRole(role_id=form.role.data)
      new_user.user_roles.append(new_user_role)
      new_user.set_password(form.email.data)
      db.session.add(new_user)
      db.session.commit()
      flash('New user created.', 'success')
      return redirect(url_for('.index'))
    else:
      flash('That email is already taken. Choose another.', 'danger')
      return redirect(url_for('.add'))
  else:
    context = {
      'form': UserForm(),
      'description': 'Create a new user',
      'title': 'Admin'
    }
    return render_template('users/add.html', **context)