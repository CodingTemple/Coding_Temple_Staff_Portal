from app import app, db
from app.models import User, Course, Role, Student, Semester, Assignment
from seed import seed_data

seed_data()

@app.shell_context_processor
def make_shell_context():
  return {
    'db': db,
    'User': User,
    'Course': Course,
    'Role': Role,
    'Student': Student,
    'Semester': Semester,
    'Assignment': Assignment
    }
