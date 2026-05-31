from dataclasses import dataclass

@dataclass
class OrderResponseDTO:
    order_id: int
    customer_name: str
    product_name: str
    total_amount: int