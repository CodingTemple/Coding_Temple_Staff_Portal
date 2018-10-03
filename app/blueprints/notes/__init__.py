from flask import abort, Blueprint, current_app, flash, redirect, request, render_template,request, url_for
from flask_login import current_user, login_required
from app.blueprints.notes.forms import NoteForm
from app.models import db, Note

from app.decorators import authorize

notes = Blueprint('notes', __name__, template_folder='templates', static_folder='static')

@notes.route('/', methods=['GET'])
@login_required
@authorize
def index():
  context = {
  }
  return render_template('notes/index.html', **context)
