from app import app
from app.models import db, User, Course, Role, Assignment, Note

from seed import add_user, add_role, add_user_role

@app.shell_context_processor
def make_shell_context():
  return {
    'db': db,
    'User': User,
    'Course': Course,
    'Role': Role,
    'Assignment': Assignment,
    'Note': Note
    }
