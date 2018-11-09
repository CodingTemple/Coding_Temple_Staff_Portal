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
    'title': 'Notes',
    'notes': Note.query.all()
  }
  return render_template('/notes/index.html', **context)

@notes.route('/edit', methods=['GET', 'POST'])
@login_required
@authorize
def edit():
  form = NoteForm()
  id = int(request.args.get('id'))
  note = Note.query.get(id)
  if request.method == 'POST':
    if form.validate_on_submit():
      if form.date.data:
        note.date = form.date.data
      note.absent = form.absent.data
      note.user_id = form.user.data
      note.note = form.note.data
      db.session.commit()
      flash('Note Updated', 'success')
      return redirect(url_for('.index'))
    else:
      flash('There was a problem adding this note', 'danger')
  else: 
    if note.date:
      form.date.data = note.date
      form.time.data = note.date
    form.absent.data = note.absent
    form.user.data = note.user_id
    form.note.data = note.note
  context = {
    'title': 'Edit ' + str(note.id),
    'form': form
  }
  return render_template('/notes/form.html', **context)

@notes.route('/delete', methods=['POST'])
@login_required
@authorize
def delete():
  id = int(request.form['id'])
  note = Note.query.get(id)
  if(note):
    db.session.delete(note)
    db.session.commit()
    flash('Note Deleted', 'success')
  return redirect(url_for('.index'))

@notes.route('/add', methods=['GET', 'POST'])
@login_required
@authorize
def add():
  form = NoteForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      note = Note(date= form.date.data, note=form.note.data, absent=form.absent.data, user_id=form.user.data )
      db.session.add(note)
      db.session.commit()
      flash('Note Added', 'success')
      return redirect(url_for('.index'))
    else:
      flash('There was a problem adding this note', 'danger')
  context = {
    'title': 'Add a Note',
    'form': form
  }
  return render_template('/notes/form.html', **context)
