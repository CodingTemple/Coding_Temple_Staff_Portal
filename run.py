from app import app
from app.models import db, User, Course, Role, Student, Semester, Assignment, Note

from seed import seed_data

@app.shell_context_processor
def make_shell_context():
  return {
    'db': db,
    'User': User,
    'Course': Course,
    'Role': Role,
    'Student': Student,
    'Semester': Semester,
    'Assignment': Assignment,
    'Note': Note
    }
