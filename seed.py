from app import app, db
from app.models import User, Role
import sqlalchemy

import click

@app.cli.command()
@click.argument('email')
@click.argument('password')
@click.argument('f_name')
@click.argument('l_name')
def add_user(email, password, f_name, l_name):
  try:
    if not User.query.filter_by(email=email).first():
      user = User(
        f_name=f_name,
        l_name=l_name,
        email=email,
        password_hash=password,
      )
      user.set_password(user.password_hash)
      db.session.add(user)
      db.session.commit()
      print('Successfully added user')
    else:
      print('User already exists')

  except Exception as error:
    print(error)
    db.session.rollback()

@app.cli.command()
@click.argument('name')
def add_role(name):
  try:
    if not Role.query.filter_by(name=name).first():
      role = Role(
        name=name,
      )
      db.session.add(role)
      db.session.commit()
      print('Successfully added role')
    else:
      print('Role already exists')

  except Exception as error:
    print(error)
    db.session.rollback()

@app.cli.command()
@click.argument('email')
@click.argument('role')
def add_user_role(email, role):
  try:
    role = Role.query.filter_by(name=role).first()
    if not role:
      raise Exception('Role does not exist')
    user = User.query.filter_by(email=email).first()
    if not user:
      raise Exception('User does not exist')
    if role not in user.roles:
      user.roles.append(role)
      db.session.commit()
      print('Added user to role')
    else:
      print('User already in role')
    
  except Exception as error:
    print(error)
    db.session.rollback()
    