

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
from sqlalchemy import and_

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    loan_count = Column(Integer)
    review_count = Column(Integer)

class BookCollection(Base):
    __tablename__ = 'book_collections'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', backref='book_collections')

class BookCollectionItem(Base):
    __tablename__ = 'book_collection_items'
    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey('book_collections.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    collection = relationship('BookCollection', backref='book_collection_items')
    book = relationship('Book', backref='book_collection_items')

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    collection_id = Column(Integer, ForeignKey('book_collections.id'))
    book = relationship('Book', backref='loans')
    collection = relationship('BookCollection', backref='loans')

class BookReview(Base):
    __tablename__ = 'book_reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    rating = Column(Float)
    book = relationship('Book', backref='book_reviews')

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    action = Column(String)
    collection_id = Column(Integer, ForeignKey('book_collections.id'))
    recommendations = Column(String)
    collection = relationship('BookCollection', backref='audit_log')

class CollectionRepository:
    def __init__(self):
        self.session = session

    def analyze_performance(self, collection_id, popularity_threshold):
        collection_data = self.session.query(BookCollection).filter_by(id=collection_id).first()
        loan_count = self.session.query(Loan).filter_by(collection_id=collection_id).count()
        review_count = self.session.query(BookReview).filter_by(book_id=collection_data.book_id).count()
        rating_average = self.session.query(func.avg(BookReview.rating)).filter_by(book_id=collection_data.book_id).first()
        if loan_count > popularity_threshold and review_count > popularity_threshold:
            performance_report = {'collection_id': collection_id, 'loan_count': loan_count, 'review_count': review_count, 'rating_average': rating_average}
            self.session.add(AuditLog(action='ANALYZE_PERFORMANCE', collection_id=collection_id, recommendations=str(performance_report)))
            self.session.commit()

    def generate_acquisition_recommendations(self, collection_id, popularity_threshold):
        collection_data = self.session.query(BookCollection).filter_by(id=collection_id == collection_id).first()
        book_collection_items = self.session.query(BookCollectionItem).filter(BookCollectionItem.collection_id == collection_id).all()
        books = self.session.query(Book).filter(Book.id.in_(book_collection_items)).all()
        loans = self.session.query(Loan).filter(Loan.book_id.in_(books)).all()
        book_reviews = self.session.query(BookReview).filter(BookReview.book_id.in_(books)).all()
        loan_count = len(loans)
        review_count = len(book_reviews)
        rating_average = sum(review.rating for review in book_reviews) / review_count if review_count > 0 else 0
        if loan_count < popularity_threshold and review_count < popularity_threshold:
            recommendations = [book.title for book in books if book.loan_count < popularity_threshold and book.review_count < popularity_threshold]
            self.session.add(AuditLog(action='GENERATE_ACQUISITION_RECOMMENDATIONS', collection_id=collection_id, recommendations=str(recommendations)))
            self.session.commit()
        return recommendations

    def rebalance_collection(self, collection_id, popularity_threshold):
        collection_data = self.session.query(BookCollection).filter_by(id=collection_id).first()
        loan_count = self.session.query(Loan).filter_by(collection_id=collection_id).count()
        review_count = self.session.query(BookReview).filter_by(book_id=collection_data.book_id).count()
        rating_average = self.session.query(func.avg(BookReview.rating)).filter_by(book_id=collection_data.book_id).first()
        if loan_count > popularity_threshold and review_count > popularity_threshold:
            recommendations = self.session.query(Book).filter_by(collection_id=collection_id).all()
            self.session.add(AuditLog(action='REBALANCE_COLLECTION', collection_id=collection_id, recommendations=str([book.title for book in recommendations])))
            self.session.commit()