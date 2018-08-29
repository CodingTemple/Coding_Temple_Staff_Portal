from app import app
from flask import render_template

@app.route('/')
def index():
  ''' 
  [GET] / \n 
  Default Route
  '''
  context = {
    'title': 'Home'
  }
  # if current_user.is_authenticated:
  #   print(current_user.role.name)
  return render_template('index.html', **context)

