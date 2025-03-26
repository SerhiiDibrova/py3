

from datetime import date

class PatronMembership:
    def __init__(self, id: int, patron_id: int, membership_plan_id: int, start_date: date, end_date: date):
        self.id = id
        self.patron_id = patron_id
        self.membership_plan_id = membership_plan_id
        self.start_date = start_date
        self.end_date = end_date