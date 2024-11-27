import os

DEBUG = True
DEBUG_DB_URI = "sqlite:////tmp/db.sqlite3"

def get_database_uri():
    if DEBUG:
        return DEBUG_DB_URI
    return os.getenv("SQLALCHEMY_DATABASE_URI")