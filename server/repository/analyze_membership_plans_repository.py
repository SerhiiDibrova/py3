

import psycopg2
import json

class AnalyzeMembershipPlansRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def analyze_membership_plans(self, p_action, p_params):
        conn = psycopg2.connect(
            dbname=self.db_config['database'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            host=self.db_config['host'],
            port=self.db_config['port']
        )
        cur = conn.cursor()

        cur.execute('''
            CREATE TEMPORARY TABLE membership_metrics (
                id INTEGER,
                name STRING,
                description STRING,
                price DECIMAL,
                loan_limit INTEGER
            )
        ''')

        cur.execute('''
            INSERT INTO membership_metrics (id, name, description, price, loan_limit)
            SELECT mp.id, mp.name, mp.description, mp.price, mp.loan_limit
            FROM membership_plans mp
            JOIN patron_memberships pm ON mp.id = pm.membership_plan_id
        ''')

        if p_action == 'ANALYZE_PERFORMANCE':
            cur.execute('''
                CREATE TEMPORARY TABLE performance_recommendations (
                    id INTEGER,
                    name STRING,
                    description STRING,
                    price DECIMAL,
                    loan_limit INTEGER,
                    total_subscriptions INTEGER,
                    active_subscriptions INTEGER,
                    average_subscription_duration DECIMAL,
                    total_revenue DECIMAL,
                    loan_utilization_rate DECIMAL,
                    reservation_utilization_rate DECIMAL
                )
            ''')

            cur.execute('''
                INSERT INTO performance_recommendations (
                    id, name, description, price, loan_limit, total_subscriptions, active_subscriptions,
                    average_subscription_duration, total_revenue, loan_utilization_rate, reservation_utilization_rate
                )
                SELECT
                    mm.id, mm.name, mm.description, mm.price, mm.loan_limit,
                    COUNT(pm.id) AS total_subscriptions,
                    COUNT(pm.id) AS active_subscriptions,
                    AVG(pm.end_date - pm.start_date) AS average_subscription_duration,
                    SUM(pm.price) AS total_revenue,
                    (COUNT(l.id) / COUNT(pm.id)) AS loan_utilization_rate,
                    (COUNT(r.id) / COUNT(pm.id)) AS reservation_utilization_rate
                FROM membership_metrics mm
                JOIN patron_memberships pm ON mm.id = pm.membership_plan_id
                LEFT JOIN loans l ON pm.id = l.patron_id
                LEFT JOIN reservations r ON pm.id = r.patron_id
                GROUP BY mm.id, mm.name, mm.description, mm.price, mm.loan_limit
            ''')

            cur.execute('''
                INSERT INTO audit_log (action, parameters, results)
                VALUES ('ANALYZE_PERFORMANCE', %s, %s)
            ''', (json.dumps(p_params), json.dumps(cur.fetchall())))

        elif p_action == 'OPTIMIZE_PRICING':
            cur.execute('''
                CREATE TEMPORARY TABLE pricing_recommendations (
                    id INTEGER,
                    name STRING,
                    description STRING,
                    price DECIMAL,
                    loan_limit INTEGER,
                    recommended_price DECIMAL,
                    price_recommendation STRING,
                    loan_limit_recommendation STRING
                )
            ''')

            cur.execute('''
                INSERT INTO pricing_recommendations (
                    id, name, description, price, loan_limit, recommended_price, price_recommendation, loan_limit_recommendation
                )
                SELECT
                    mm.id, mm.name, mm.description, mm.price, mm.loan_limit,
                    (mm.price * (1 + %s)) AS recommended_price,
                    'Increase price by ' || %s || '%' AS price_recommendation,
                    'Increase loan limit by ' || %s || '%' AS loan_limit_recommendation
                FROM membership_metrics mm
            ''', (p_params['optimization_threshold'], p_params['optimization_threshold'], p_params['optimization_threshold']))

            cur.execute('''
                INSERT INTO audit_log (action, parameters, results)
                VALUES ('OPTIMIZE_PRICING', %s, %s)
            ''', (json.dumps(p_params), json.dumps(cur.fetchall())))

        cur.execute('DROP TABLE membership_metrics')
        if p_action == 'ANALYZE_PERFORMANCE':
            cur.execute('DROP TABLE performance_recommendations')
        elif p_action == 'OPTIMIZE_PRICING':
            cur.execute('DROP TABLE pricing_recommendations')

        conn.commit()
        cur.close()
        conn.close()