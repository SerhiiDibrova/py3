

package client.src.data_access

import client.src.database.Database

class ProgramStatusDataAccess:
    def update_program_status(self, program_id, completion_rate):
        Database().update_program_status(program_id, completion_rate)