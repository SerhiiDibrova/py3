

from flask import current_app as app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from client.models import EventRegistration

def register_for_event(p_event_id, p_patron_id):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    db = Session()
    new_registration = EventRegistration(event_id=p_event_id, patron_id=p_patron_id)
    db.add(new_registration)
    db.commit()