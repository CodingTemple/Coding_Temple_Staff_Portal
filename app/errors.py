from flask import render_template
from app import app
from app.models import db

@app.errorhandler(404)
def not_found_error(error):
  context = {
    'title': '404 Error'
  }
  return render_template('errors/404.html', **context), 404

@app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  context = {
    'title': '500 Error'
  }
  return render_template('errors/500.html', **context), 500

@app.errorhandler(401)
def unauthorized_error(error):
  context = {
    'title': '401 Error'
  }
  return render_template('errors/401.html', **context), 404
