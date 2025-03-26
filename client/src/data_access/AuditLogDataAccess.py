

package client.src.data_access

import client.src.database.Database

class AuditLogDataAccess:
    def log_completion_statistics(self, program_id, completion_rate):
        Database.log_database(program_id, completion_rate)