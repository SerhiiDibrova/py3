

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def analyze_membership_plans(p_action, p_params):
    engine = create_engine('postgresql://user:password@host:port/dbname')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.execute(text("CREATE TEMPORARY TABLE membership_metrics (id INTEGER, name STRING, description STRING, price DECIMAL, loan_limit INTEGER)"))

    session.execute(text("INSERT INTO membership_metrics (id, name, description, price, loan_limit) SELECT mp.id, mp.name, mp.description, mp.price, mp.loan_limit FROM membership_plans mp JOIN patron_memberships pm ON mp.id = pm.membership_plan_id"))

    if p_action == 'ANALYZE_PERFORMANCE':
        session.execute(text("CREATE TEMPORARY TABLE performance_recommendations (id INTEGER, name STRING, description STRING, price DECIMAL, loan_limit INTEGER, total_subscriptions INTEGER, active_subscriptions INTEGER, average_subscription_duration DECIMAL, total_revenue DECIMAL, loan_utilization_rate DECIMAL, reservation_utilization_rate DECIMAL)"))

        session.execute(text("INSERT INTO performance_recommendations (id, name, description, price, loan_limit, total_subscriptions, active_subscriptions, average_subscription_duration, total_revenue, loan_utilization_rate, reservation_utilization_rate) SELECT mm.id, mm.name, mm.description, mm.price, mm.loan_limit, COUNT(pm.id) AS total_subscriptions, COUNT(pm.id) AS active_subscriptions, AVG(pm.end_date - pm.start_date) AS average_subscription_duration, SUM(pm.price) AS total_revenue, (COUNT(l.id) / COUNT(pm.id)) AS loan_utilization_rate, (COUNT(r.id) / COUNT(pm.id)) AS reservation_utilization_rate FROM membership_metrics mm JOIN patron_memberships pm ON mm.id = pm.membership_plan_id LEFT JOIN loans l ON pm.id = l.patron_id LEFT JOIN reservations r ON pm.id = r.patron_id GROUP BY mm.id, mm.name, mm.description, mm.price, mm.loan_limit"))

        session.execute(text("INSERT INTO audit_log (action, parameters, results) VALUES ('ANALYZE_PERFORMANCE', :p_params, (SELECT json_agg(row_to_json(performance_recommendations)) FROM performance_recommendations))"), {'p_params': p_params})

    elif p_action == 'OPTIMIZE_PRICING':
        session.execute(text("CREATE TEMPORARY TABLE pricing_recommendations (id INTEGER, name STRING, description STRING, price DECIMAL, loan_limit INTEGER, recommended_price DECIMAL, price_recommendation STRING, loan_limit_recommendation STRING)"))

        session.execute(text("INSERT INTO pricing_recommendations (id, name, description, price, loan_limit, recommended_price, price_recommendation, loan_limit_recommendation) SELECT mm.id, mm.name, mm.description, mm.price, mm.loan_limit, (mm.price * (1 + :optimization_threshold)) AS recommended_price, 'Increase price by ' || :optimization_threshold || '%' AS price_recommendation, 'Increase loan limit by ' || :optimization_threshold || '%' AS loan_limit_recommendation FROM membership_metrics mm"), {'optimization_threshold': p_params['optimization_threshold']})

        session.execute(text("INSERT INTO audit_log (action, parameters, results) VALUES ('OPTIMIZE_PRICING', :p_params, (SELECT json_agg(row_to_json(pricing_recommendations)) FROM pricing_recommendations))"), {'p_params': p_params})