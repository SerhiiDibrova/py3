

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class AnalyzeCollectionPerformanceBusinessLogic:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)

    def create_temp_table(self, collection_id):
        query = text("CREATE TEMPORARY TABLE collection_analysis AS SELECT * FROM Book_Collections WHERE collection_id = :collection_id")
        try:
            with self.engine.connect() as conn:
                conn.execute(query, collection_id=collection_id)
        except SQLAlchemyError as e:
            logging.error(f"Error creating temporary table: {e}")

    def populate_temp_table(self, collection_id):
        query = text("""
            INSERT INTO collection_analysis (collection_id, book_id, loan_count, review_count)
            SELECT 
                bc.collection_id,
                bci.book_id,
                COALESCE(l.loan_count, 0),
                COALESCE(br.review_count, 0)
            FROM 
                Book_Collections bc
            JOIN 
                Book_Collection_Items bci ON bc.collection_id = bci.collection_id
            LEFT JOIN 
                Loans l ON bci.book_id = l.book_id
            LEFT JOIN 
                Book_Reviews br ON bci.book_id = br.book_id
            WHERE 
                bc.collection_id = :collection_id
        """)
        try:
            with self.engine.connect() as conn:
                conn.execute(query, collection_id=collection_id)
        except SQLAlchemyError as e:
            logging.error(f"Error populating temporary table: {e}")

    def generate_performance_report(self, collection_id):
        query = text("""
            INSERT INTO Audit_Log (collection_id, report_type, report_data)
            SELECT 
                :collection_id,
                'performance_report',
                JSON_AGG(row_to_json(t))
            FROM (
                SELECT 
                    collection_id,
                    book_id,
                    loan_count,
                    review_count
                FROM 
                    collection_analysis
            ) t
        """)
        try:
            with self.engine.connect() as conn:
                conn.execute(query, collection_id=collection_id)
        except SQLAlchemyError as e:
            logging.error(f"Error generating performance report: {e}")

    def drop_temp_table(self, collection_id):
        query = text("DROP TABLE collection_analysis")
        try:
            with self.engine.connect() as conn:
                conn.execute(query)
        except SQLAlchemyError as e:
            logging.error(f"Error dropping temporary table: {e}")

    def analyze_performance(self, collection_id, params):
        self.create_temp_table(collection_id)
        self.populate_temp_table(collection_id)
        self.generate_performance_report(collection_id)
        self.drop_temp_table(collection_id)

    def generate_acquisition_recommendations(self, collection_id, params):
        self.create_temp_table(collection_id)
        self.populate_temp_table(collection_id)
        # TO DO: implement acquisition recommendations logic
        self.drop_temp_table(collection_id)

    def rebalance_collection(self, collection_id, params):
        self.create_temp_table(collection_id)
        self.populate_temp_table(collection_id)
        # TO DO: implement rebalancing logic
        self.drop_temp_table(collection_id)