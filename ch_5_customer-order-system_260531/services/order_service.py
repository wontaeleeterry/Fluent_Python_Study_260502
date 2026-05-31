from entities.order import OrderEntity
from vo.money import Money


class OrderService:

    def __init__(self):

        from repositories.order_repository \
            import OrderRepository

        self.order_repo = OrderRepository()

    def create_order(self, dto):

        order = OrderEntity(
            id=None,
            customer_id=dto.customer_id,
            product_name=dto.product_name,
            total_amount=Money(
                dto.total_amount
            )
        )

        self.order_repo.save(order)