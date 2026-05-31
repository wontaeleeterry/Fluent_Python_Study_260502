from dataclasses import dataclass

@dataclass
class CreateOrderDTO:
    customer_id: int
    product_name: str
    total_amount: int