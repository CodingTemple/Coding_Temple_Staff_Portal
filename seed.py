from app import app, db
from app.models import User, Role, Course, userRole
import sqlalchemy

@app.cli.command()
def seed_data():
  try:

    if Role.query.all() is None or not Role.query.all():
      db.session.add_all([Role(name=i) for i in ["Super User", "Instructor", "Student"]])
      db.session.commit()
    
    if User.query.all() is None or not User.query.all():
      user = User(
        f_name="Derek",
        l_name="Hawkins",
        email="derek@codingtemple.com",
        password_hash=app.config['SUPER_USER_PASSWORDS'][0],
      )
      user.set_password(user.password_hash)
      db.session.add(user)
      db.session.commit()
    
    if not Role.query.filter_by(name="Super User").first().users.all():
      user = User.query.filter_by(email = "derek@codingtemple.com").first()
      role = Role.query.filter_by(name = "Super User").first()
      user.roles.append(role)
      db.session.commit()
    
  except sqlalchemy.exc.SQLAlchemyError:
    db.session.rollback()