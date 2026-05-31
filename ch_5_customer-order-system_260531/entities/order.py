from dataclasses import dataclass

@dataclass
class OrderEntity:
    id: int | None
    customer_id: int
    product_name: str
    total_amount: Money