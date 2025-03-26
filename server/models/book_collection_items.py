

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BookCollectionItems(Base):
    __tablename__ = 'book_collection_items'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    collection_id = Column(Integer, ForeignKey('book_collections.id'))

    def __init__(self, id, book_id, collection_id):
        self.id = id
        self.book_id = book_id
        self.collection_id = collection_id