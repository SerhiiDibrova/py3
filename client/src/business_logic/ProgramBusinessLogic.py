

package client.src.business_logic

import logging
from client.src.data_access import ProgramDataAccess
from client.src.utils import calculate_completion_rate

class ProgramBusinessLogic:
    def __init__(self):
        self.program_data_access = ProgramDataAccess()
        self.logger = logging.getLogger(__name__)

    def calculate_completion_statistics_business_logic(self, program_id):
        program_data = self.program_data_access.retrieve_program_data(program_id)
        completion_rate = calculate_completion_rate(program_data)
        self.program_data_access.update_program_status(program_id, completion_rate)
        self.log_completion_statistics(program_id, completion_rate)
        return completion_rate

    def log_completion_statistics(self, program_id, completion_rate):
        self.logger.info(f"Program {program_id} completion rate: {completion_rate}")