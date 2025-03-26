

from datetime import datetime, timedelta
from typing import Dict
import uuid

class InterlibraryLoanService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def process_interlibrary_loan_request(self, patron_id: int, requesting_branch_id: int, book_title: str, isbn: str, providing_institution: str) -> str:
        # Validate patron status
        patron_status = self.validate_patron_status(patron_id)
        if patron_status != 'active':
            raise ValueError('Patron is not active')

        # Check for pending fines
        pending_fines = self.check_pending_fines(patron_id)
        if pending_fines > 0:
            raise ValueError('Patron has pending fines')

        # Calculate expected arrival date and cost
        expected_arrival_date, cost = self.calculate_expected_arrival_date_and_cost(requesting_branch_id, providing_institution)

        # Insert request into database
        ill_id = self.insert_request_into_database(patron_id, requesting_branch_id, book_title, isbn, providing_institution, expected_arrival_date, cost)

        return ill_id

    def validate_patron_status(self, patron_id: int) -> str:
        # Query to validate patron status
        query = "SELECT status FROM patrons WHERE id = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (patron_id,))
        result = cursor.fetchone()
        return result[0]

    def check_pending_fines(self, patron_id: int) -> float:
        # Query to check pending fines
        query = "SELECT SUM(amount) FROM fines WHERE patron_id = %s AND paid = FALSE"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (patron_id,))
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def calculate_expected_arrival_date_and_cost(self, requesting_branch_id: int, providing_institution: str) -> (datetime, float):
        # Calculate expected arrival date and cost based on the requesting branch and providing institution
        # For simplicity, assume a fixed cost and arrival date
        expected_arrival_date = datetime.now() + timedelta(days=7)
        cost = 5.0
        return expected_arrival_date, cost

    def insert_request_into_database(self, patron_id: int, requesting_branch_id: int, book_title: str, isbn: str, providing_institution: str, expected_arrival_date: datetime, cost: float) -> str:
        # Query to insert request into database
        query = "INSERT INTO interlibrary_loan_requests (patron_id, requesting_branch_id, book_title, isbn, providing_institution, expected_arrival_date, cost) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (patron_id, requesting_branch_id, book_title, isbn, providing_institution, expected_arrival_date, cost))
        ill_id = cursor.fetchone()[0]
        self.db_connection.commit()
        return ill_id