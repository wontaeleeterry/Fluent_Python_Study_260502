"""
main.py

프로그램 시작점(Entry Point)

실행 흐름

1. 고객 생성
2. 주문 생성
3. 주문 조회
4. DTO 출력
"""

from vo.email import Email

from entities.customer import CustomerEntity

from dto.create_order_dto import CreateOrderDTO

from repositories.customer_repository import (
    CustomerRepository
)

from services.order_service import (
    OrderService
)

from repositories.order_repository import (
    OrderRepository
)

from dto.order_response_dto import (
    OrderResponseDTO
)


def main():

    print("=" * 50)
    print("쇼핑몰 주문 시스템 시작")
    print("=" * 50)

    # --------------------------------------------------
    # 1. 고객 등록
    # --------------------------------------------------

    customer_repo = CustomerRepository()

    customer = CustomerEntity(
        id=None,
        name="홍길동",
        email=Email("hong@test.com")
    )

    customer_id = customer_repo.save(customer)

    print()
    print("고객 등록 완료")
    print(f"고객 ID: {customer_id}")

    # --------------------------------------------------
    # 2. 주문 생성
    # --------------------------------------------------

    create_order_dto = CreateOrderDTO(
        customer_id=customer_id,
        product_name="MacBook Pro M6",
        total_amount=3500000
    )

    service = OrderService()

    service.create_order(create_order_dto)

    print()
    print("주문 생성 완료")

    # --------------------------------------------------
    # 3. 주문 조회
    # --------------------------------------------------

    order_repo = OrderRepository()

    rows = order_repo.find_all()

    print()
    print("=" * 50)
    print("주문 목록")
    print("=" * 50)

    # --------------------------------------------------
    # 4. Entity -> DTO 변환
    # --------------------------------------------------

    for row in rows:

        response = OrderResponseDTO(
            order_id=row[0],
            customer_name=row[1],
            product_name=row[2],
            total_amount=row[3]
        )

        print(response)

    print()
    print("프로그램 종료")


if __name__ == "__main__":
    main()