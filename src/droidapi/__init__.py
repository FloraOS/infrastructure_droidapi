__author__ = "Anna-Sophie Zaitsewa"
__email__ = "f104a@f104a.io"
__version__ = "0.1.5"

import os

from droidapi import app
from droidapi.db import Base, get_db_session, engine
from droidapi.config import DEBUG

# Add your endpoints specification imports here
from droidapi.endpoints.update import *
from droidapi.endpoints.status import *
from droidapi.endpoints.media import *
from droidapi.helpers.authorization import generate_token

if DEBUG:
    # We override some parametes here, just in case someone tries to run debug app on production
    app.config["SECRET_KEY"] = '12345'
    app.config["UPLOAD_FOLDER"] = '/tmp'
    app.config["UPLOADS_URL"] = 'http://127.0.0.1:5000/updates/'
    print("!! App running in debug mode, DB and secrets parameters are overriden to avoid data loss and breaches")
else:
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
    app.config["UPLOADS_URL"] = os.getenv("UPLOADS_URL")

with app.app_context():
    Base.metadata.create_all(bind=engine)
    if DEBUG:
        print(":: Initialized database with tables: ", Base.metadata.tables.keys())
        _session = get_db_session()
        model, token = generate_token(app.config["SECRET_KEY"])
        _session.add(model)
        _session.commit()
        del _session # We do not what it accidently being accessible somewhere else
        print(":: Your debug access token is " + token)
