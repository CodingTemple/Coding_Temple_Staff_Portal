# Setting up a Flask app

This is a starter template for creating a flask application. The instructions are as follows:

## Clone the repository
## Create your virtual environment
### MacOS/Linux:
#### mkdir myproject
#### cd myproject
#### python3 -m venv venv
### Windows:
#### mkdir myproject
#### cd myproject
#### py -3 -m venv venv
## Activate your Virtual Environment
### MacOS/Linux:
#### . venv/bin/activate
### Windows:
#### venv\Scripts\activate
## In your terminal, set your FLASK_APP variable to run.py
### MacOS/Linux:
##### export FLASK_APP=run.py
### Windows:
##### set FLASK_APP=run.py
### Powershell
##### $Env:FLASK_APP = "run.py"
## In your terminal, install all of the required modules
### Windows/Linux/MacOS:
##### pip install -r requirements.txt

## Manage PIP dependencies
### Anytime you install something via pip install, be sure to:
#### pip freeze > requirements.txt

## db migrations
### flask db upgrade

## Seed User
$Env:SU_1 = "password"
flask seed_data