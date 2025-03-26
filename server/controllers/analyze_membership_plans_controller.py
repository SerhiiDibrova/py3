

import json
import logging
from typing import Dict

from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AnalyzeMembershipPlansController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_membership_plans(self, p_action: str, p_params: Dict) -> Dict:
        try:
            # Create temporary table membership_metrics
            membership_metrics = db.Table('membership_metrics', db.metadata,
                                          db.Column('id', db.Integer),
                                          db.Column('name', db.String),
                                          db.Column('description', db.String),
                                          db.Column('price', db.DECIMAL),
                                          db.Column('loan_limit', db.Integer))

            # Populate membership_metrics with data from membership_plans and patron_memberships tables
            db.session.execute(membership_metrics.insert().from_select(
                ['id', 'name', 'description', 'price', 'loan_limit'],
                db.select([db.func.mp.id, db.func.mp.name, db.func.mp.description, db.func.mp.price, db.func.mp.loan_limit])
                .select_from(db.func.mp.join(db.func.pm, db.func.mp.id == db.func.pm.membership_plan_id))
            ))

            if p_action == 'ANALYZE_PERFORMANCE':
                # Create temporary table performance_recommendations
                performance_recommendations = db.Table('performance_recommendations', db.metadata,
                                                       db.Column('id', db.Integer),
                                                       db.Column('name', db.String),
                                                       db.Column('description', db.String),
                                                       db.Column('price', db.DECIMAL),
                                                       db.Column('loan_limit', db.Integer),
                                                       db.Column('total_subscriptions', db.Integer),
                                                       db.Column('active_subscriptions', db.Integer),
                                                       db.Column('average_subscription_duration', db.DECIMAL),
                                                       db.Column('total_revenue', db.DECIMAL),
                                                       db.Column('loan_utilization_rate', db.DECIMAL),
                                                       db.Column('reservation_utilization_rate', db.DECIMAL))

                # Insert into performance_recommendations
                db.session.execute(performance_recommendations.insert().from_select(
                    ['id', 'name', 'description', 'price', 'loan_limit', 'total_subscriptions', 'active_subscriptions',
                     'average_subscription_duration', 'total_revenue', 'loan_utilization_rate', 'reservation_utilization_rate'],
                    db.select([
                        db.func.mm.id, db.func.mm.name, db.func.mm.description, db.func.mm.price, db.func.mm.loan_limit,
                        db.func.count(db.func.pm.id).label('total_subscriptions'),
                        db.func.count(db.func.pm.id).label('active_subscriptions'),
                        db.func.avg(db.func.pm.end_date - db.func.pm.start_date).label('average_subscription_duration'),
                        db.func.sum(db.func.pm.price).label('total_revenue'),
                        (db.func.count(db.func.l.id) / db.func.count(db.func.pm.id)).label('loan_utilization_rate'),
                        (db.func.count(db.func.r.id) / db.func.count(db.func.pm.id)).label('reservation_utilization_rate')
                    ])
                    .select_from(db.func.mm.join(db.func.pm, db.func.mm.id == db.func.pm.membership_plan_id))
                    .outerjoin(db.func.l, db.func.pm.id == db.func.l.patron_id)
                    .outerjoin(db.func.r, db.func.pm.id == db.func.r.patron_id)
                    .group_by(db.func.mm.id, db.func.mm.name, db.func.mm.description, db.func.mm.price, db.func.mm.loan_limit)
                ))

                # Insert into audit_log
                db.session.execute(db.func.audit_log.insert().values(
                    action='ANALYZE_PERFORMANCE',
                    parameters=json.dumps(p_params),
                    results=json.dumps([dict(row) for row in db.session.query(performance_recommendations).all()])
                ))

            elif p_action == 'OPTIMIZE_PRICING':
                # Create temporary table pricing_recommendations
                pricing_recommendations = db.Table('pricing_recommendations', db.metadata,
                                                   db.Column('id', db.Integer),
                                                   db.Column('name', db.String),
                                                   db.Column('description', db.String),
                                                   db.Column('price', db.DECIMAL),
                                                   db.Column('loan_limit', db.Integer),
                                                   db.Column('recommended_price', db.DECIMAL),
                                                   db.Column('price_recommendation', db.String),
                                                   db.Column('loan_limit_recommendation', db.String))

                # Insert into pricing_recommendations
                db.session.execute(pricing_recommendations.insert().from_select(
                    ['id', 'name', 'description', 'price', 'loan_limit', 'recommended_price', 'price_recommendation',
                     'loan_limit_recommendation'],
                    db.select([
                        db.func.mm.id, db.func.mm.name, db.func.mm.description, db.func.mm.price, db.func.mm.loan_limit,
                        (db.func.mm.price * (1 + p_params['optimization_threshold'])).label('recommended_price'),
                        ('Increase price by ' + str(p_params['optimization_threshold']) + '%').label('price_recommendation'),
                        ('Increase loan limit by ' + str(p_params['optimization_threshold']) + '%').label('loan_limit_recommendation')
                    ])
                    .select_from(db.func.mm)
                ))

                # Insert into audit_log
                db.session.execute(db.func.audit_log.insert().values(
                    action='OPTIMIZE_PRICING',
                    parameters=json.dumps(p_params),
                    results=json.dumps([dict(row) for row in db.session.query(pricing_recommendations).all()])
                ))

            # Drop temporary tables
            db.session.execute('DROP TABLE membership_metrics')
            if p_action == 'ANALYZE_PERFORMANCE':
                db.session.execute('DROP TABLE performance_recommendations')
            elif p_action == 'OPTIMIZE_PRICING':
                db.session.execute('DROP TABLE pricing_recommendations')

            return jsonify({'message': 'Membership plans analyzed successfully'}), 200

        except Exception as e:
            self.logger.error(f'Error analyzing membership plans: {str(e)}')
            return jsonify({'message': 'Error analyzing membership plans'}), 500