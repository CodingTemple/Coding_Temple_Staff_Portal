from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for, jsonify
from flask_login import current_user, login_required
from app.blueprints.users.forms import UserForm
from app.models import User, Role, db, Note

from app.decorators import authorize

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')

@users.route('/', methods=['GET'])
@login_required
@authorize
def index():
  rid = request.args.get('role')
  if rid is not None:
    users = Role.query.get(rid).users
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
        user.roles = Role.query.filter(Role.id == form.role.data).all()
        db.session.commit()
        flash('Updated user ' + uid, 'success') 
        return redirect(url_for('.index'))
    flash('Could not update user.', 'danger')
  form.f_name.data = user.f_name
  form.l_name.data = user.l_name
  if(user.roles) :
    form.role.data = user.roles[0].id
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
      new_user_role = Role.query.get(form.role.data)
      new_user.roles.append(new_user_role)
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

@users.route('/lookup', methods=['GET'])
@login_required
@authorize
def lookup():
  s = request.args.get('s') or ''
  users = [{'id':user.id,'fname':user.f_name, 'lname':user.l_name, 'email':user.email} for user in User.query.filter(User.email.contains(s) | User.f_name.contains(s) | User.l_name.contains(s)).all()]
  return jsonify(users)