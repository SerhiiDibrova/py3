

import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patron_memberships (
                membership_id INTEGER PRIMARY KEY,
                patron_id INTEGER,
                plan_id INTEGER,
                end_date DATE,
                auto_renewal BOOLEAN,
                price DECIMAL,
                duration_months INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS membership_plans (
                plan_id INTEGER PRIMARY KEY,
                name STRING,
                description STRING
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patrons (
                patron_id INTEGER PRIMARY KEY,
                email STRING,
                first_name STRING,
                last_name STRING,
                PRIMARY KEY (patron_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fines (
                fine_id INTEGER PRIMARY KEY,
                patron_id INTEGER,
                amount DECIMAL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY,
                patron_id INTEGER,
                item_id INTEGER,
                due_date DATE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id INTEGER PRIMARY KEY,
                table_name STRING,
                record_id INTEGER,
                action_type STRING,
                action_timestamp TIMESTAMP,
                new_values JSONB
            )
        ''')

        self.conn.commit()

    def insert_patron_membership(self, membership):
        self.cursor.execute('''
            INSERT INTO patron_memberships (
                membership_id,
                patron_id,
                plan_id,
                end_date,
                auto_renewal,
                price,
                duration_months
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?
            )
        ''', (
            membership.membership_id,
            membership.patron_id,
            membership.plan_id,
            membership.end_date,
            membership.auto_renewal,
            membership.price,
            membership.duration_months
        ))

        self.conn.commit()

    def get_patron_membership(self, membership_id):
        self.cursor.execute('''
            SELECT * FROM patron_memberships
            WHERE membership_id = ?
        ''', (membership_id,))

        return self.cursor.fetchone()

    def insert_audit_log(self, table_name, record_id, action_type, new_values):
        self.cursor.execute('''
            INSERT INTO audit_log (
                table_name,
                record_id,
                action_type,
                action_timestamp,
                new_values
            ) VALUES (
                ?, ?, ?, ?, ?
            )
        ''', (
            table_name,
            record_id,
            action_type,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            json.dumps(new_values)
        ))

        self.conn.commit()

    def get_audit_log(self, log_id):
        self.cursor.execute('''
            SELECT * FROM audit_log
            WHERE log_id = ?
        ''', (log_id,))

        return self.cursor.fetchone()

    def insert_patron(self, patron):
        self.cursor.execute('''
            INSERT INTO patrons (
                patron_id,
                email,
                first_name,
                last_name
            ) VALUES (
                ?, ?, ?, ?
            )
        ''', (
            patron.patron_id,
            patron.email,
            patron.first_name,
            patron.last_name
        ))

        self.conn.commit()

    def get_patron(self, patron_id):
        self.cursor.execute('''
            SELECT * FROM patrons
            WHERE patron_id = ?
        ''', (patron_id,))

        return self.cursor.fetchone()

    def insert_membership_plan(self, plan):
        self.cursor.execute('''
            INSERT INTO membership_plans (
                plan_id,
                name,
                description
            ) VALUES (
                ?, ?, ?
            )
        ''', (
            plan.plan_id,
            plan.name,
            plan.description
        ))

        self.conn.commit()

    def get_membership_plan(self, plan_id):
        self.cursor.execute('''
            SELECT * FROM membership_plans
            WHERE plan_id = ?
        ''', (plan_id,))

        return self.cursor.fetchone()

    def insert_fine(self, fine):
        self.cursor.execute('''
            INSERT INTO fines (
                fine_id,
                patron_id,
                amount
            ) VALUES (
                ?, ?, ?
            )
        ''', (
            fine.fine_id,
            fine.patron_id,
            fine.amount
        ))

        self.conn.commit()

    def get_fine(self, fine_id):
        self.cursor.execute('''
            SELECT * FROM fines
            WHERE fine_id = ?
        ''', (fine_id,))

        return self.cursor.fetchone()

    def insert_loan(self, loan):
        self.cursor.execute('''
            INSERT INTO loans (
                loan_id,
                patron_id,
                item_id,
                due_date
            ) VALUES (
                ?, ?, ?, ?
            )
        ''', (
            loan.loan_id,
            loan.patron_id,
            loan.item_id,
            loan.due_date
        ))

        self.conn.commit()

    def get_loan(self, loan_id):
        self.cursor.execute('''
            SELECT * FROM loans
            WHERE loan_id = ?
        ''', (loan_id,))

        return self.cursor.fetchone()