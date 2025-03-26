

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    publication_date = Column(Date)

    def __init__(self, id, title, author, publisher, publication_date):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publication_date = publication_date