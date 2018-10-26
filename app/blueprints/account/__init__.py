from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.blueprints.account.forms import LoginForm, RegistrationForm, ProfileForm
from app.models import User, db
from app import app
import time, os
from datetime import date

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')

@account.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    u = User(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data)
    u.set_password(form.password.data)
    db.session.add(u)
    db.session.commit()
    flash('You are registered', 'success')
    return redirect(url_for('account.login'))
  context = {
    'form': RegistrationForm(),
    'description': 'Register',
    'title': 'Register'
  }
  return render_template('account/register.html', **context)

@account.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    if current_user.role.name == 'Super User':
      return redirect(url_for('admin.index'))
    return redirect(url_for('index'))
  form = LoginForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      u = User.query.filter_by(email=form.email.data).first()
      if u is None or not u.check_password(form.password.data):
        flash('Invalid email or password. Try again.', 'danger')
        return redirect(url_for('account.login'))
      login_user(u, remember=form.remember_me.data)
      flash('You are logged in.', 'success')
      return redirect(url_for('index'))
    flash('CSRF or form failure. Try again.', 'danger')
    return redirect(url_for('account.login'))
  context = {
    'form': LoginForm(),
    'description': 'Login',
    'title': 'Login'
  }
  return render_template('account/login.html', **context)

@account.route('/logout')
def logout():
  logout_user()
  flash('You are logged out.', 'success')
  return redirect(url_for('account.login'))

@login_required
@account.route('/', methods=['GET', 'POST'])
def index():
  form = ProfileForm()
  if not current_user.is_authenticated:
    return redirect(url_for('index'))
  if form.validate_on_submit():
    print("form is valid")
    user = User.query.get(current_user.id)
    user.f_name = form.first_name.data
    user.l_name = form.last_name.data
    user.email = form.email.data
    user.bio = form.bio.data
    if not os.path.exists(app.config['PROFILE_PICS_FOLDER']):
      print("created folder")
      os.makedirs(app.config['PROFILE_PICS_FOLDER'])
    filename = str(int(time.time())) + '.png'
    print(os.path.join(app.config['PROFILE_PICS_FOLDER'], filename))
    form.image.data.save(os.path.join(app.config['PROFILE_PICS_FOLDER'], filename))
    user.image = filename
    db.session.commit()
    print("data commited")
    flash('Profile edited successfully', 'success')
    return redirect(url_for('account.index'))
  context = {
    'title': 'Profile',
    'description': 'Profile',
    'form': form,
  }
  return render_template('account/index.html', **context)
