from app import app, db
from app.models import User, Role, Course
import sqlalchemy

@app.cli.command()
def seed_data():
  try:
    if User.query.all() is None or not User.query.all():
      user = User(
        f_name="Derek",
        l_name="Hawkins",
        email="derek@codingtemple.com",
        password_hash=app.config['SUPER_USER_PASSWORDS'][0],
        role_id=1
      )
      user.set_password(user.password_hash)
      db.session.add(user)
    
    if Role.query.all() is None or not Role.query.all():
      db.session.add_all([Role(name=i) for i in ["Super User", "Administrator", "Student"]])
    
    db.create_all()
    db.session.commit()
  except sqlalchemy.exc.SQLAlchemyError:
    db.session.rollback()