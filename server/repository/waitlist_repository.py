

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

engine = create_engine('postgresql://user:password@localhost/dbname')
Base = declarative_base()

class Waitlist(Base):
    __tablename__ = 'waitlist'
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer)
    patron_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_waitlist_table():
    Base.metadata.create_all(engine)

def update_waitlist_table(waitlist_data):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(waitlist_data)
    session.commit()

def retrieve_waitlist_data(program_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    waitlist_data = session.query(Waitlist).filter_by(program_id=program_id).all()
    return waitlist_data

def create_waitlist_notification_batch(program_id):
    waitlist_data = retrieve_waitlist_data(program_id)
    for waitlist in waitlist_data:
        send_email(waitlist.patron_id, 'Waitlist Notification', 'You have been added to the waitlist for the program.')

def send_email(patron_id, subject, body):
    msg = MIMEMultipart()
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'patron-email@gmail.com'
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], 'your-password')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()