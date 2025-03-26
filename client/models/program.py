

from pydantic import BaseModel

class Program(BaseModel):
    program_id: int
    status: str
    session_schedule: dict
    min_participants: int