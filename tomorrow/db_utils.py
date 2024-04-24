from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tomorrow.models import Base

def setup_database(url):
    """
    Creates database engine, initializes tables if they don't exist,
    and returns a sessionmaker.
    """
    engine = create_engine(url) 
    Base.metadata.create_all(engine)  
    return sessionmaker(bind=engine)

def get_session(url):
    """
    Get a new session from the session factory.
    """
    Session = setup_database(url)
    return Session()
