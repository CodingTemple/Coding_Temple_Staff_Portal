from flask import abort, Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app.forms import AdminForm
from app.models import User, db

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@login_required
@admin.route('/', methods=['GET', 'POST'])
def index():
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
  return render_template('admin/index.html', **context)