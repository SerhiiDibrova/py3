

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class BookCollections(Base):
    __tablename__ = 'book_collections'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def create(self, db):
        session = sessionmaker(bind=db)()
        session.add(self)
        session.commit()

    def read(self, db):
        session = sessionmaker(bind=db)()
        return session.query(BookCollections).filter_by(id=self.id).first()

    def update(self, db):
        session = sessionmaker(bind=db)()
        session.query(BookCollections).filter_by(id=self.id).update({'name': self.name, 'description': self.description})
        session.commit()

    def delete(self, db):
        session = sessionmaker(bind=db)()
        session.query(BookCollections).filter_by(id=self.id).delete()
        session.commit()