import functools
from datetime import datetime

from flask import request

from droidapi.db.models.statictoken import StaticToken
from droidapi.db import db

def authorized_only(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        if "X-DroidAPI-Token" not in request.headers:
            return 401, {"status": "unauthorized"}
        token = request.headers["X-DroidAPI-Token"]
        models = db.session.execute(db.select(StaticToken).where(StaticToken.token == token)).fetchall()
        if len(models) == 0:
            return 401, {"status": "unauthorized"}
        if len(models) > 1:
            raise ValueError("Multiple StaticTokens found")
        model = models[0]
        time = datetime.now()
        if time > model.expires_at or time < model.created_at:
            return 401, {"status": "unauthorized"}
        return func(*args, **kwargs)
    return decorated