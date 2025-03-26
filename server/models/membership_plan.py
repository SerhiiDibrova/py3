

from dataclasses import dataclass

@dataclass
class MembershipPlan:
    id: int
    name: str
    description: str
    price: float
    loan_limit: int