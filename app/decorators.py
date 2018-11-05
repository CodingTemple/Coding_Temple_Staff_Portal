from functools import wraps
from flask import abort, g, request, redirect, url_for
from flask_login import current_user, login_required

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Super User" not in map(lambda r: r.name, current_user.roles):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
