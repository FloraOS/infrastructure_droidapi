from droidapi import app
from droidapi.db import db

# Add your endpoints specification imports here
from droidapi.endpoints.update import *
from droidapi.endpoints.status import *
from droidapi.helpers.authorization import generate_token

DEBUG = True

if DEBUG:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite://'
    app.config["SECRET_KEY"] = '12345'
    print("!! App running in debug mode, DB and secrets parameters are overriden to avoid data loss and breaches")
db.init_app(app)

with app.app_context():
    db.create_all()
    if DEBUG:
        model, token = generate_token(app.config["SECRET_KEY"])
        db.session.add(model)
        db.session.commit()
        print(":: Your debug access token is " + token)
