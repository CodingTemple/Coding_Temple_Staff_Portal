from app import app, db
from flask import redirect, render_template, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, AdminForm
from app.models import User

@app.route('/')
def index():
  context = {
    'title': 'Home'
  }
  # if current_user.is_authenticated:
  #   print(current_user.role.name)
  return render_template('index.html', **context)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    u = User(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data)
    u.set_password(form.password.data)
    db.session.add(u)
    db.session.commit()
    flash("You are registered", "success")
    return redirect(url_for('login'))
  context = {
    'form': RegistrationForm(),
    'description': 'Register',
    'title': 'Register'
  }
  return render_template('authentication/register.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    if current_user.role.name == 'Super User':
      return redirect(url_for('admin'))
    return redirect(url_for('index'))
  form = LoginForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      u = User.query.filter_by(email=form.email.data).first()
      if u is None or not u.check_password(form.password.data):
        flash('Invalid email or password. Try again.', 'danger')
        return redirect(url_for('login'))
      login_user(u, remember=form.remember_me.data)
      flash('You are logged in.', 'success')
      return redirect(url_for('index'))
    flash('CSRF or form failure. Try again.', 'danger')
    return redirect(url_for('login'))
  context = {
    'form': LoginForm(),
    'description': 'Login',
    'title': 'Login'
  }
  return render_template('authentication/login.html', **context)

@app.route('/logout')
def logout():
  logout_user()
  flash('You are logged out.', 'success')
  return redirect(url_for('login'))


@login_required
@app.route('/admin', methods=['GET', 'POST'])
def admin():
  if not current_user.is_authenticated or not current_user.role.name == 'Super User':
    flash('You are not authorized to view this page.', 'danger')
    return redirect(url_for('index'))
  form = AdminForm()
  if form.validate_on_submit():
    print(form.role.data)
    print("begin validation...")
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None:
      flash('That email is already taken. Choose another.', 'danger')
      return redirect(url_for('admin'))
    new_user = User(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, role_id=form.role.data)
    new_user.set_password(form.email.data)
    db.session.add(new_user)
    db.session.commit()
    flash('New user created.', 'success')
    return redirect(url_for('admin'))
  context = {
    'form': AdminForm(),
    'description': 'Create a new user',
    'title': 'Admin'
  }
  return render_template('admin/admin.html', **context)
