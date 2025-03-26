

from datetime import date

class InterlibraryLoan:
    def __init__(self, requesting_branch_id, patron_id, book_title, isbn, providing_institution, expected_arrival, cost):
        self.requesting_branch_id = requesting_branch_id
        self.patron_id = patron_id
        self.book_title = book_title
        self.isbn = isbn
        self.providing_institution = providing_institution
        self.expected_arrival = expected_arrival
        self.cost = cost