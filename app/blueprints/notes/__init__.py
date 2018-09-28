from flask import Blueprint, request, flash, render_template, redirect, url_for
from app.models import Note

notes = Blueprint('notes', __name__, template_folder='templates', static_folder='static')

@notes.route('/')
def index():
  context = {
    'title': 'Notes',
    'notes': Note.query.all()
  }
  return render_template('/notes/index.html', **context)