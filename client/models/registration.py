

from pydantic import BaseModel

class Registration(BaseModel):
    registration_id: int
    program_id: int
    patron_id: int
    attendance_log: dict
    payment_status: str