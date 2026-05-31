from dataclasses import dataclass

@dataclass
class CustomerEntity:
    id: int | None
    name: str
    email: Email