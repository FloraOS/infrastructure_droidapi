from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from droidapi.config import get_database_uri

engine = create_engine(
    get_database_uri(),
    pool_pre_ping=True
)

Session = scoped_session(sessionmaker(bind=engine))

def get_db_session():
    """Return a scoped session."""
    return Session()

Base = declarative_base()