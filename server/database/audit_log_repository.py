

import psycopg2
from psycopg2 import Error

class AuditLogRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def insert_log_entry(self, collection_id, action, log_date):
        try:
            connection = psycopg2.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Audit_Log (collection_id, action, log_date) VALUES (%s, %s, %s)', (collection_id, action, log_date))
            connection.commit()
        except Error as e:
            print(f"Error occurred while inserting log entry: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_log_data(self, collection_id):
        try:
            connection = psycopg2.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Audit_Log WHERE collection_id = %s', (collection_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error occurred while retrieving log data: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()