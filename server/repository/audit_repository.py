

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2
from datetime import datetime

class AuditRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def log_audit_report(self, patron_id, patron_record, activity_report):
        log_values = {
            'patron_id': patron_id,
            'action': 'AUDIT_ACTIVITY',
            'timestamp': datetime.now(),
            'activity_report': activity_report
        }

        query = text("INSERT INTO audit_log (patron_id, action, timestamp, activity_report) VALUES (:patron_id, :action, :timestamp, :activity_report)")
        with self.Session() as session:
            session.execute(query, log_values)
            session.commit()

    def execute_query(self, query, params):
        try:
            conn = psycopg2.connect(
                host='localhost',
                database='chat_app',
                user='chat_app_user',
                password='chat_app_password'
            )
            cur = conn.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except psycopg2.Error as e:
            print(f'Error: {e}')
            return None