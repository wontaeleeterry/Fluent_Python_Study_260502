import sqlite3
from dataclasses import dataclass
from typing import List


# ==========================================================
# User 데이터 구조 정의
# ==========================================================
#
# 데이터베이스에 저장된 사용자 정보를
# 프로그램 내부에서는 User 객체로 다룬다.
#
@dataclass
class User:
    id: int
    username: str
    email: str
    age: int


# ==========================================================
# 데이터베이스 초기화
# ==========================================================
#
# users 테이블을 생성하고
# 샘플 데이터를 삽입한다.
#
def initialize_database() -> None:

    conn = sqlite3.connect("example_260530.db")

    try:
        cursor = conn.cursor()

        # 기존 테이블 제거
        cursor.execute("DROP TABLE IF EXISTS users")

        # 새 테이블 생성
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)

        # 샘플 데이터 삽입
        cursor.executemany(
            """
            INSERT INTO users
            (username, email, age)
            VALUES (?, ?, ?)
            """,
            [
                ("alice", "alice@test.com", 22),
                ("bob", "bob@test.com", 31),
                ("charlie", "charlie@test.com", 17),
                ("david", "david@test.com", 45)
            ]
        )

        conn.commit()

    finally:
        conn.close()


# ==========================================================
# DB 데이터를 User 객체로 변환
# ==========================================================
#
# SELECT 결과는 tuple 형태로 반환된다.
#
# 예:
# (1, 'alice', 'alice@test.com', 22)
#
# 이를 User 객체로 변환한다.
#
def get_users() -> List[User]:

    conn = sqlite3.connect("example_260530.db")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                username,
                email,
                age
            FROM users
        """)

        rows = cursor.fetchall()

        users = []

        for row in rows:

            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                age=row[3]
            )

            users.append(user)

        return users

    finally:
        conn.close()


# ==========================================================
# 비즈니스 로직
# ==========================================================
#
# 성인 사용자만 필터링한다.
#
def get_adult_users(users: List[User]) -> List[User]:

    return [
        user
        for user in users
        if user.age >= 20
    ]


# ==========================================================
# 비즈니스 로직
# ==========================================================
#
# 이메일 도메인 추출
#
def get_email_domain(user: User) -> str:

    return user.email.split("@")[1]


# ==========================================================
# 메인 프로그램
# ==========================================================
#
# 전체 흐름:
#
# SQLite
#    ↓
# User 객체
#    ↓
# 비즈니스 로직
#    ↓
# 출력
#
def main():

    initialize_database()   # 데이터베이스 생성 (260530)

    users = get_users()     # 데이터베이스에 저장된 데이터 가져오기

    print("=== 전체 사용자 ===")

    for user in users:
        print(user)

    print()
    print("=== 성인 사용자 ===")

    adults = get_adult_users(users)   # 조건(성인)에 따른 user 분류

    for user in adults:               # 분류된 결과를 보기 좋게 출력

        domain = get_email_domain(user)

        print(
            f"{user.username:<10}"    # 인덱스 대신 컬럼명으로 출력 가능
            f" 나이={user.age:<3}"
            f" 이메일도메인={domain}"
        )


if __name__ == "__main__":
    main()