project/

├── main.py

├── entities/
│   ├── customer.py
│   └── order.py

├── dto/
│   ├── create_order_dto.py
│   └── order_response_dto.py

├── vo/
│   ├── email.py
│   └── money.py

├── repositories/
│   ├── customer_repository.py
│   └── order_repository.py

├── services/
│   └── order_service.py

└── database.py


실무에서는 main.py가 단순히 객체를 생성하는 파일이 아니라 애플리케이션의 시작점(Entry Point) 역할을 합니다.

앞서 만든 구조를 기준으로 하면 다음과 같은 시나리오를 구현할 수 있습니다.

1. 고객 등록
2. 주문 생성
3. 주문 조회
4. DTO 형태로 출력