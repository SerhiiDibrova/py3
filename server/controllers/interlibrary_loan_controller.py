

```python
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from exceptions import PatronAccountInactiveException, PendingFinesException

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    account_status = Column(String)

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    amount = Column(Float)

class InterlibraryLoan(Base):
    __tablename__ = 'interlibrary_loans'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    requesting_branch_id = Column(Integer)
    book_title = Column(String)
    isbn = Column(String)
    providing_institution = Column(String)
    expected_arrival_date = Column(DateTime)
    cost = Column(Float)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    interlibrary_loan_id = Column(Integer)
    tracking_date = Column(DateTime)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class InterlibraryLoanController:
    def __init__(self, patron_id, requesting_branch_id, book_title, isbn, providing_institution):
        self.patron_id = patron_id
        self.requesting_branch_id = requesting_branch_id
        self.book_title = book_title
        self.isbn = isbn
        self.providing_institution = providing_institution

    def validate_patron_status(self):
        patron = session.query(Patron).filter_by(id=self.patron_id).first()
        if patron.account_status != 'active':
            raise PatronAccountInactiveException

    def check_pending_fines(self):
        fine = session.query(Fine).filter_by(patron_id=self.patron_id).first()
        if fine:
            raise PendingFinesException

    def calculate_expected_arrival(self):
        return datetime.now() + timedelta(days=7)

    def calculate_cost(self):
        return 15.00

    def insert_request_into_database(self):
        ill = InterlibraryLoan(
            patron_id=self.patron_id,
            requesting_branch_id=self.requesting_branch_id,
            book_title=self.book_title,
            isbn=self.isbn,
            providing_institution=self.providing_institution,
            expected_arrival_date=self.calculate_expected_arrival(),
            cost=self.calculate_cost()
        )
        session.add(ill)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        return ill.id

    def create_tracking_record(self, ill_id):
        tracking = AuditLog(
            interlibrary_loan_id=ill_id,
            tracking_date=datetime.now()
        )
        session.add(tracking)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        return tracking.id
```