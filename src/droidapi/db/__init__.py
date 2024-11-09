from flask_sqlalchemy import SQLAlchemy

from droidapi.db.models import BaseModel

db = SQLAlchemy(model_class=BaseModel)