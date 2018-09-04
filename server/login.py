""" 04.09.18 - Check for login wrapper """
from functools import wraps
from flask import session, redirect, url_for, request


def requires_login(func):
    @wraps(func)
    def login_function(*args, **kwargs):
        if 'user' not in session.keys() or not session['user']:
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    return login_function
