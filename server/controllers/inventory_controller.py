

package server.controllers;

import logging
import sqlite3
from server.models.inventory import Inventory
from server.models.audit_log import AuditLog

class InventoryController:
    def __init__(self):
        self.threshold_config = {
            'damage_threshold': 0.2,
            'reorder_threshold': 0.5
        }

    def audit_inventory(self, branch_id, action, params):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Create a temporary table for current inventory status
        cursor.execute('''
            CREATE TEMPORARY TABLE current_inventory AS
            SELECT * FROM inventory WHERE branch_id = ?
        ''', (branch_id,))

        # Perform specified action: AUDIT_INVENTORY
        if action == 'AUDIT_INVENTORY':
            # Create a temporary table for audit results
            cursor.execute('''
                CREATE TEMPORARY TABLE audit_results AS
                SELECT * FROM current_inventory WHERE quantity != ?
            ''', (params['expected_quantity'],))

            # Process discrepancies and update inventory records
            cursor.execute('''
                UPDATE inventory SET quantity = ?
                WHERE branch_id = ? AND item_id = ?
            ''', (params['expected_quantity'], branch_id, params['item_id']))

            # Log discrepancies in audit log
            audit_log = AuditLog(branch_id, 'AUDIT_INVENTORY', params)
            audit_log.log_discrepancy()

            # Drop audit results table
            cursor.execute('DROP TABLE audit_results')

        conn.commit()
        conn.close()

    def process_damages(self, branch_id, action, params):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Update inventory records for damaged items
        cursor.execute('''
            UPDATE inventory SET quantity = quantity - ?
            WHERE branch_id = ? AND item_id = ?
        ''', (params['damage_quantity'], branch_id, params['item_id']))

        # Update inventory record status based on damage threshold
        cursor.execute('''
            UPDATE inventory SET status = ?
            WHERE branch_id = ? AND item_id = ?
        ''', ('DAMAGED' if params['damage_quantity'] > self.threshold_config['damage_threshold'] else 'ACTIVE', branch_id, params['item_id']))

        conn.commit()
        conn.close()

    def reorder_analysis(self, branch_id, action, params):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Create a temporary table for reorder recommendations
        cursor.execute('''
            CREATE TEMPORARY TABLE reorder_recommendations AS
            SELECT * FROM inventory WHERE quantity < ?
        ''', (params['reorder_threshold'],))

        # Generate recommendations based on inventory status and threshold configuration
        cursor.execute('''
            SELECT * FROM reorder_recommendations WHERE quantity < ?
        ''', (params['reorder_threshold'] * self.threshold_config['reorder_threshold'],))

        # Log recommendations in audit log
        audit_log = AuditLog(branch_id, 'REORDER_ANALYSIS', params)
        audit_log.log_recommendation()

        # Drop recommendations table
        cursor.execute('DROP TABLE reorder_recommendations')

        conn.commit()
        conn.close()