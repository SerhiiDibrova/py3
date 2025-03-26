

import datetime
import json
import psycopg2

def generate_monthly_statistics(p_year, p_month):
    v_start_date = datetime.date(p_year, p_month, 1)
    v_end_date = v_start_date + datetime.timedelta(days=31)
    v_end_date = v_end_date.replace(day=1) - datetime.timedelta(days=1))

    conn = psycopg2.connect(
        database="library",
        user="library_user",
        password="library_password",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TEMPORARY TABLE monthly_stats AS
        SELECT 
            COUNT(*) AS total_loans,
            SUM(CASE WHEN due_date < %s THEN 1 ELSE 0 END) AS overdue_loans,
            SUM(CASE WHEN return_date IS NULL THEN 1 ELSE 0 END) AS active_borrowers,
            SUM(fine_amount) AS total_fines,
            SUM(CASE WHEN paid_date IS NOT NULL THEN fine_amount ELSE 0 END) AS paid_fines,
            SUM(CASE WHEN paid_date IS NULL THEN fine_amount ELSE 0 END) AS pending_fines,
            COUNT(*) AS books_in_circulation,
            SUM(available_copies) AS total_available_copies,
            AVG(rating) AS average_rating,
            COUNT(*) AS total_events,
            SUM(participant_count) AS total_participants,
            AVG(capacity_utilization) AS average_capacity_utilization
        FROM 
            loans
            LEFT JOIN fines ON loans.loan_id = fines.loan_id
            LEFT JOIN books ON loans.book_id = books.book_id
            LEFT JOIN book_reviews ON books.book_id = book_reviews.book_id
            LEFT JOIN library_events ON library_events.event_date BETWEEN %s AND %s
        WHERE 
            loans.loan_date BETWEEN %s AND %s
            OR fines.issue_date BETWEEN %s AND %s
            OR books.review_date BETWEEN %s AND %s
            OR library_events.event_date BETWEEN %s AND %s
    """, (v_start_date, v_start_date, v_end_date, v_start_date, v_end_date, v_start_date, v_end_date, v_start_date, v_end_date, v_start_date, v_end_date))

    cur.execute("SELECT * FROM monthly_stats")
    monthly_stats = cur.fetchone()

    cur.execute("""
        INSERT INTO audit_log (report_name, report_date, action, timestamp, report_data)
        VALUES (%s, %s, %s, %s, %s)
    """, ('monthly_statistics', v_start_date, 'INSERT', datetime.datetime.now(), json.dumps(monthly_stats)))

    cur.execute("DROP TABLE monthly_stats")

    conn.commit()
    conn.close()