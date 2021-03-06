# Coding Temple Staff Portal

## Running the Application

- [ ] Clone the repository

- [ ] Create your virtual environment

### MacOS/Linux Virtual Environement Creation

```Shell
mkdir myproject
cd myproject
python3 -m venv venv
```

### Windows Virtual Environement Creation

```Shell
mkdir myproject
cd myproject
py -3 -m venv venv
```

- [ ] Activate your Virtual Environment

### MacOS/Linux Environment Activation

```Shell
. venv/bin/activate
```

### Windows Environment Activation

```Shell
venv\Scripts\activate
```

- [ ] In your terminal, set your environment variables

### MacOS/Linux Environment Variables

```Shell
export FLASK_APP=run.py
export FLASK_DEBUG=1
export FLASK_ENV=development
```

### Windows Environment Variables

```Shell
set FLASK_APP=run.py
set FLASK_DEBUG=1
set FLASE_ENV=development
```

### Powershell Environment Variables

```PowerShell
$Env:FLASK_APP = "run.py"
$Env:FLASK_DEBUG = 1
$Env:FLASK_ENV = "development"
```

- [ ]  In your terminal, install all of the required modules

```Shell
pip install -r requirements.txt
```python

- [ ] Run the app

```Shell
flask run
```

## Manage PIP dependencies

Anytime you install something via pip install, be sure to freeze the new dependency in requirements.txt

```Shell
pip freeze > requirements.txt
```

## db migrations

The application should automatically migrate when run, but can be manually executed with the command:

```Shell
flask db upgrade
```

## Seed User

```Shell
flask add_user <email> <password> <firstname> <lastname>

flask add_role <role>

flask add_user_role <email> <role>

```