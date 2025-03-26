

from datetime import date, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, and_, or_, not_
from json import dumps

Base = declarative_base()

class MonthlyStatistics(Base):
    __tablename__ = 'monthly_statistics'
    id = Column(Integer, primary_key=True)
    total_loans = Column(Integer)
    overdue_loans = Column(Integer)
    active_borrowers = Column(Integer)
    total_fines = Column(Float)
    paid_fines = Column(Float)
    pending_fines = Column(Float)
    books_in_circulation = Column(Integer)
    total_available_copies = Column(Integer)
    average_rating = Column(Float)
    total_events = Column(Integer)
    total_participants = Column(Integer)
    average_capacity_utilization = Column(Float)

def generate_monthly_statistics(p_year, p_month):
    start_date = date(p_year, p_month, 1)
    end_date = start_date + timedelta(days=31)
    engine = create_engine('postgresql://user:password@host:port/dbname')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    loan_stats = session.query(func.count(Loans.id).label('total_loans'), 
                               func.sum(func.case([(Loans.due_date < start_date, 1)], else_=0)).label('overdue_loans'), 
                               func.sum(func.case([(Loans.return_date == None, 1)], else_=0)).label('active_borrowers')).\
                               filter(Loans.loan_date.between(start_date, end_date)).first()

    fine_stats = session.query(func.sum(Fines.fine_amount).label('total_fines'), 
                               func.sum(func.case([(Fines.paid_date != None, Fines.fine_amount)], else_=0)).label('paid_fines'), 
                               func.sum(func.case([(Fines.paid_date == None, Fines.fine_amount)], else_=0)).label('pending_fines')).\
                               filter(Fines.issue_date.between(start_date, end_date)).first()

    book_stats = session.query(func.count(Books.id).label('books_in_circulation'), 
                               func.sum(Books.available_copies).label('total_available_copies'), 
                               func.avg(BookReviews.rating).label('average_rating')).\
                               filter(or_(Books.review_date.between(start_date, end_date), Books.review_date == None)).first()

    event_stats = session.query(func.count(LibraryEvents.id).label('total_events'), 
                                func.sum(LibraryEvents.participant_count).label('total_participants'), 
                                func.avg(LibraryEvents.capacity_utilization).label('average_capacity_utilization')).\
                                filter(LibraryEvents.event_date.between(start_date, end_date)).first()

    monthly_stats = MonthlyStatistics(total_loans=loan_stats.total_loans, 
                                      overdue_loans=loan_stats.overdue_loans, 
                                      active_borrowers=loan_stats.active_borrowers, 
                                      total_fines=fine_stats.total_fines, 
                                      paid_fines=fine_stats.paid_fines, 
                                      pending_fines=fine_stats.pending_fines, 
                                      books_in_circulation=book_stats.books_in_circulation, 
                                      total_available_copies=book_stats.total_available_copies, 
                                      average_rating=book_stats.average_rating, 
                                      total_events=event_stats.total_events, 
                                      total_participants=event_stats.total_participants, 
                                      average_capacity_utilization=event_stats.average_capacity_utilization)

    session.add(monthly_stats)
    session.commit()

    session.query(MonthlyStatistics).delete()
    session.commit()