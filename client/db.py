

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

def get_db_session():
    Session = sessionmaker(bind=engine)
    return Session()