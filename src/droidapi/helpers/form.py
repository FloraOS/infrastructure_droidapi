import functools

from flask import request

def need_form_fields(fields):
    """
    Checks that form passed in request contains needed fields
    :param fields: fields needed by endpoint to be in form
    :return: decorated function
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            for field in fields:
                if field not in request.form:
                    return {"status": "missing_field"}, 400
            return f(*args, **kwargs)
        return decorated
    return decorator