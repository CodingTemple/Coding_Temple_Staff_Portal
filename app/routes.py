from app import app
from flask import render_template, redirect, url_for
from flask_login import current_user

@app.route('/')
def index():
  ''' 
  [GET] / \n 
  Default Route
  '''
  if current_user.is_anonymous:
    return redirect(url_for('account.login'))
  context = {
    'title': 'Home'
  }
  # if current_user.is_authenticated:
  #   print(current_user.role.name)
  return render_template('index.html', **context)