

from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class CollectionRepository:
    def __init__(self):
        self.session = sessionmaker(bind=engine)()

    def analyze_and_manage_collections(self, action, collection_id):
        try:
            self.session.execute('CREATE TEMPORARY TABLE collection_metrics (id INTEGER, name VARCHAR(255), description VARCHAR(255), total_loans INTEGER, recent_loans INTEGER, average_rating REAL, category_distribution JSONB)')
            self.session.execute('INSERT INTO collection_metrics (id, name, description, total_loans, recent_loans, average_rating, category_distribution) SELECT bc.id, bc.name, bc.description, COUNT(DISTINCT l.id) AS total_loans, COUNT(DISTINCT l.id) FILTER (WHERE l.loan_date > NOW() - INTERVAL \'1 year\') AS recent_loans, AVG(br.rating) AS average_rating, JSONB_AGG(DISTINCT bc.category) AS category_distribution FROM Book_Collections bc JOIN Book_Collection_Items bci ON bc.id = bci.collection_id JOIN Books b ON bci.book_id = b.id JOIN Loans l ON b.id = l.book_id JOIN Book_Reviews br ON b.id = br.book_id GROUP BY bc.id, bc.name, bc.description')
            if action == 'ANALYZE_PERFORMANCE':
                self.session.execute('INSERT INTO Audit_Log (action, collection_id, recommendations) SELECT \'ANALYZE_PERFORMANCE\', p_collection_id, JSONB_BUILD_OBJECT(\'recommendations\', cm.total_loans, \'recent_loans\', cm.recent_loans, \'average_rating\', cm.average_rating) FROM collection_metrics cm')
            elif action == 'GENERATE_ACQUISITION_RECOMMENDATIONS':
                self.session.execute('INSERT INTO Audit_Log (action, collection_id, recommendations) SELECT \'GENERATE_ACQUISITION_RECOMMENDATIONS\', p_collection_id, JSONB_BUILD_OBJECT(\'recommendations\', cm.category_distribution) FROM collection_metrics cm')
            elif action == 'REBALANCE_COLLECTION':
                self.session.execute('INSERT INTO Audit_Log (action, collection_id, recommendations) SELECT \'REBALANCE_COLLECTION\', p_collection_id, JSONB_BUILD_OBJECT(\'recommendations\', cm.total_loans, \'recent_loans\', cm.recent_loans, \'average_rating\', cm.average_rating) FROM collection_metrics cm')
            self.session.execute('INSERT INTO Audit_Log (action, collection_id, recommendations) VALUES (\'ANALYSIS_COMPLETE\', p_collection_id, NULL)')
            self.session.execute('DROP TABLE collection_metrics')
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def create_collection(self, collection_data):
        self.session.execute('INSERT INTO book_collections (name, description) VALUES (:name, :description)', collection_data)
        self.session.commit()

    def get_collection(self, collection_id):
        result = self.session.execute('SELECT * FROM book_collections WHERE id = :id', {'id': collection_id})
        return result.fetchone()

    def update_collection(self, collection_id, collection_data):
        self.session.execute('UPDATE book_collections SET name = :name, description = :description WHERE id = :id', collection_data)
        self.session.commit()

    def delete_collection(self, collection_id):
        self.session.execute('DELETE FROM book_collections WHERE id = :id', {'id': collection_id})
        self.session.commit()