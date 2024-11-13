__author__ = "Anna-Sophie Zaitsewa"
__email__ = "f104a@f104a.io"
__version__ = "0.1.0"

from droidapi import app
from droidapi.db import db

# Add your endpoints specification imports here
from droidapi.endpoints.update import *
from droidapi.endpoints.status import *
from droidapi.endpoints.media import *
from droidapi.helpers.authorization import generate_token

DEBUG = False

if DEBUG:
    # We override some parametes here, just in case someone tries to run debug app on production
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite://'
    app.config["SECRET_KEY"] = '12345'
    app.config["UPLOAD_FOLDER"] = '/tmp'
    app.config["UPLOADS_URL"] = 'http://127.0.0.1:5000/updates/'
    print("!! App running in debug mode, DB and secrets parameters are overriden to avoid data loss and breaches")

db.init_app(app)

with app.app_context():
    db.create_all()
    if DEBUG:
        model, token = generate_token(app.config["SECRET_KEY"])
        db.session.add(model)
        db.session.commit()
        print(":: Your debug access token is " + token)
