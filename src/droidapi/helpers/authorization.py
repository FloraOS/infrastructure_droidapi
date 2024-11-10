import functools
import _sha512
import string
import secrets
from datetime import datetime, timedelta
from typing import Tuple

from click import Tuple
from flask import request

from droidapi.db.models.statictoken import StaticToken
from droidapi.db import db
from droidapi.app import app

def authorized_only(func):
    """
    Decorates route function to be accessible only for authorized users.
    :param func: function to decorate
    :return: Decorated function
    """
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        if "X-DroidAPI-Token" not in request.headers:
            return {"status": "unauthorized"}, 401
        token = _sha512.sha512((request.headers["X-DroidAPI-Token"] + app.config['SECRET_KEY']).encode()).hexdigest()
        models = db.session.execute(db.select(StaticToken).where(StaticToken.token == token)).fetchall()
        if len(models) == 0:
            return {"status": "unauthorized"}, 401
        if len(models) > 1:
            raise ValueError("Multiple StaticTokens found")
        model = models[0][0]
        time = datetime.now()
        if time > model.expires_at or time < model.issued_at:
            return {"status": "unauthorized"}, 401
        request.current_token = model
        return func(*args, **kwargs)
    return decorated


def generate_secure_string(length=128, chars=string.ascii_letters + string.digits) -> str:
    """
    Generate a cryptographically secure random string.

    Parameters:
        length (int): Length of the resulting string.
        chars (str): Characters to choose from for the string.

    Returns:
        str: A cryptographically secure random string.
    """
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_token(secret_key, length=128, expire_days=7) -> tuple[StaticToken, str]:
    """
    Generates access token returning its model and unhashed token
    :param: secret_key: apps' secret key
    :param length: length of the token
    :return: Tuple[StaticToken, str]: StaticToken model and unhashed token
    """
    model = StaticToken()
    unhashed_token =  generate_secure_string(length)
    model.token = _sha512.sha512((unhashed_token +  secret_key).encode()).hexdigest()
    model.issued_at = datetime.now()
    model.expires_at = datetime.now() + timedelta(days=expire_days)
    return model, unhashed_token