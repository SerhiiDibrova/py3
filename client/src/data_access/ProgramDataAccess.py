

package client.src.data_access

import sqlite3

class ProgramDataAccess:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def retrieve_program_data(self, program_id):
        self.cursor.execute("SELECT * FROM programs WHERE id=?", (program_id,))
        program_data = self.cursor.fetchone()
        return program_data

    def close_connection(self):
        self.conn.close()