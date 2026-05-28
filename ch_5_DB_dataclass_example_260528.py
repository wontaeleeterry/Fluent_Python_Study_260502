# 필요한 라이브러리 임포트
import sqlite3
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, date

# ============================================================
# 1. 도메인 레이어: dataclass로 데이터 구조 정의
#    - DB 테이블 구조와 1:1 매핑되지 않아도 됨
#    - 비즈니스 로직에 필요한 형태로 자유롭게 설계
# ============================================================

@dataclass
class Employee:
    """직원 기본 정보 - DB의 employees 테이블과 매핑"""
    id: int
    name: str
    department: str
    salary: float
    hire_date: str
    
    # DB에는 없는 가공 필드 (프로퍼티로 계산)
    @property
    def years_employed(self) -> int:
        """입사일로부터 근속 연수 계산"""
        hire_year = int(self.hire_date.split('-')[0])
        return datetime.now().year - hire_year
    
    @property
    def monthly_salary(self) -> float:
        """연봉 → 월급 변환"""
        return round(self.salary / 12, 2)


@dataclass  
class DepartmentSummary:
    """부서별 통계 - 여러 테이블을 조인한 결과를 담는 DTO"""
    department: str
    employee_count: int
    avg_salary: float
    total_salary: float
    
    @property
    def avg_salary_formatted(self) -> str:
        return f"{self.avg_salary:,.0f}원"


@dataclass
class HighEarner:
    """고액 연봉자 정보 - 특정 조건 필터링 결과용 DTO"""
    name: str
    department: str
    salary: float
    percentile: Optional[float] = None  # 나중에 계산해서 채울 수 있음


# ============================================================
# 2. DB 레이어: SQLite 연결 및 데이터 조작
# ============================================================

def create_connection(db_path: str = ":memory:") -> sqlite3.Connection:
    """
    SQLite 연결 생성
    - ':memory:' 는 메모리 내 임시 DB (테스트/학습용)
    - 실제 파일로 저장하려면 'company.db' 같은 경로 지정
    """
    conn = sqlite3.connect(db_path)
    # row_factory 설정: 쿼리 결과를 dict처럼 접근 가능하게 함
    # 기본은 tuple이라 conn.row_factory 없으면 row[0], row[1]로만 접근
    conn.row_factory = sqlite3.Row
    return conn


def setup_database(conn: sqlite3.Connection) -> None:
    """테이블 생성 및 샘플 데이터 삽입"""
    cursor = conn.cursor()
    
    # 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            department  TEXT NOT NULL,
            salary      REAL NOT NULL,
            hire_date   TEXT NOT NULL
        )
    """)
    
    # 샘플 데이터 삽입
    # executemany: 리스트의 각 튜플을 반복 삽입 (효율적)
    sample_data = [
        ("김민준", "개발팀",   85000000, "2019-03-15"),
        ("이서연", "개발팀",   92000000, "2018-07-22"),
        ("박지훈", "마케팅팀", 67000000, "2021-01-10"),
        ("최수아", "마케팅팀", 71000000, "2020-05-30"),
        ("정도윤", "개발팀",   110000000,"2016-11-05"),
        ("강하은", "인사팀",   58000000, "2022-08-18"),
        ("윤재원", "인사팀",   63000000, "2021-04-25"),
        ("임지수", "개발팀",   78000000, "2020-09-12"),
        ("한승호", "마케팅팀", 55000000, "2023-02-01"),
        ("오나연", "개발팀",   95000000, "2017-06-30"),
    ]
    
    cursor.executemany(
        "INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
        sample_data
    )
    conn.commit()
    print("✅ DB 초기화 완료\n")


# ============================================================
# 3. Repository 레이어: SQL 실행 + dataclass 변환
#    - SQL 결과(raw Row)를 dataclass로 변환하는 책임
#    - 비즈니스 로직은 여기 넣지 않음
# ============================================================

def fetch_all_employees(conn: sqlite3.Connection) -> list[Employee]:
    """
    모든 직원 조회 → Employee dataclass 리스트 반환
    
    sqlite3.Row → dict(**row) → dataclass 변환 흐름:
    row['name'] 처럼 컬럼명으로 접근 가능 (row_factory 덕분)
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees ORDER BY salary DESC")
    rows = cursor.fetchall()
    
    # 각 Row를 Employee dataclass로 변환
    # dict(row): sqlite3.Row → 일반 dict로 변환
    # Employee(**dict(row)): dict를 키워드 인자로 풀어서 생성
    return [Employee(**dict(row)) for row in rows]


def fetch_department_summary(conn: sqlite3.Connection) -> list[DepartmentSummary]:
    """
    부서별 집계 통계 조회
    - SQL에서 GROUP BY로 집계한 결과를 DepartmentSummary로 변환
    - DB가 무거운 연산을 처리하고, Python은 결과만 받음 (효율적)
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            department,
            COUNT(*)        AS employee_count,
            AVG(salary)     AS avg_salary,
            SUM(salary)     AS total_salary
        FROM employees
        GROUP BY department
        ORDER BY avg_salary DESC
    """)
    rows = cursor.fetchall()
    
    return [
        DepartmentSummary(
            department     = row['department'],
            employee_count = row['employee_count'],
            avg_salary     = round(row['avg_salary'], 2),
            total_salary   = row['total_salary']
        )
        for row in rows
    ]


def fetch_high_earners(conn: sqlite3.Connection, threshold: float) -> list[HighEarner]:
    """
    특정 연봉 이상인 직원 조회
    - threshold: 기준 연봉 (파라미터 바인딩으로 SQL 인젝션 방지)
    - ? 플레이스홀더에 (threshold,) 튜플로 값 전달
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, department, salary
        FROM employees
        WHERE salary >= ?
        ORDER BY salary DESC
    """, (threshold,))  # ← 반드시 튜플로! (threshold) 는 그냥 괄호, (threshold,) 가 튜플
    
    rows = cursor.fetchall()
    return [
        HighEarner(
            name       = row['name'],
            department = row['department'],
            salary     = row['salary']
        )
        for row in rows
    ]


# ============================================================
# 4. 서비스 레이어: dataclass를 받아서 비즈니스 로직 처리
#    - DB를 전혀 모름, dataclass만 다룸
#    - 테스트하기 쉬움 (DB 없이도 단위 테스트 가능)
# ============================================================

def calculate_salary_percentile(employees: list[Employee], target: Employee) -> float:
    """
    특정 직원의 연봉 백분위 계산
    - DB에서 꺼낸 dataclass 리스트를 순수 Python 로직으로 처리
    """
    salaries = sorted([e.salary for e in employees])
    rank = salaries.index(target.salary)
    return round((rank / len(salaries)) * 100, 1)


def enrich_high_earners(
    high_earners: list[HighEarner], 
    all_employees: list[Employee]
) -> list[HighEarner]:
    """
    고액 연봉자 DTO에 백분위 정보 추가 (데이터 보강)
    - dataclass는 frozen=True가 아니면 필드값 수정 가능
    """
    all_salaries = sorted([e.salary for e in all_employees])
    
    for earner in high_earners:
        rank = all_salaries.index(earner.salary)
        earner.percentile = round((rank / len(all_salaries)) * 100, 1)
    
    return high_earners


def filter_by_seniority(employees: list[Employee], min_years: int) -> list[Employee]:
    """
    근속 연수로 필터링 - dataclass의 @property 활용
    - years_employed 는 DB 컬럼이 아닌 계산 필드
    """
    return [e for e in employees if e.years_employed >= min_years]


# ============================================================
# 5. 메인 실행: 전체 흐름 시연
# ============================================================

def main():
    # --- DB 연결 및 초기화 ---
    conn = create_connection(":memory:")
    setup_database(conn)
    
    # ── 예제 1: 전체 직원 조회 + dataclass 프로퍼티 활용 ──
    print("=" * 55)
    print("📋 전체 직원 목록 (연봉 내림차순)")
    print("=" * 55)
    
    employees = fetch_all_employees(conn)
    
    for emp in employees:
        print(
            f"  {emp.name:<6} | {emp.department:<8} | "
            f"연봉: {emp.salary:>12,.0f}원 | "
            f"월급: {emp.monthly_salary:>10,.0f}원 | "
            f"근속: {emp.years_employed}년"
            # monthly_salary, years_employed 는 DB에 없는 계산 필드
        )
    
    # ── 예제 2: 부서별 통계 (SQL GROUP BY → DTO) ──
    print("\n" + "=" * 55)
    print("📊 부서별 연봉 통계")
    print("=" * 55)
    
    summaries = fetch_department_summary(conn)
    
    for s in summaries:
        print(
            f"  {s.department:<8} | "
            f"인원: {s.employee_count}명 | "
            f"평균연봉: {s.avg_salary_formatted:<15} | "  # 포맷된 프로퍼티 사용
            f"총인건비: {s.total_salary:>14,.0f}원"
        )
    
    # ── 예제 3: 조건 필터링 + 서비스 로직으로 데이터 보강 ──
    print("\n" + "=" * 55)
    print("💰 고액 연봉자 (8000만원 이상) + 백분위")
    print("=" * 55)
    
    # 고액 연봉자 조회 쿼리에서 결과 값 전달 받음 (260528)
    high_earners = fetch_high_earners(conn, threshold=80_000_000)
    # DB에서 받은 DTO에 백분위 정보를 Python 로직으로 추가
    high_earners = enrich_high_earners(high_earners, employees)
    
    # 전달 받은 쿼리 결과에서 필요한 정보를 추출함 (260528)
    for earner in high_earners:
        print(
            f"  {earner.name:<6} | {earner.department:<8} | "
            f"{earner.salary:>12,.0f}원 | "
            f"상위 {100 - earner.percentile:.0f}%"
        )
    
    # ── 예제 4: DB 쿼리 없이 순수 Python으로 필터링 ──
    print("\n" + "=" * 55)
    print("🏆 5년 이상 근속자 (dataclass 프로퍼티로 필터)")
    print("=" * 55)
    
    # employees 는 이미 메모리에 있음 → DB 재조회 불필요
    veterans = filter_by_seniority(employees, min_years=5)
    
    for emp in veterans:
        print(f"  {emp.name:<6} | {emp.department:<8} | 근속 {emp.years_employed}년")
    
    # ── 예제 5: dataclass를 dict로 변환 (API 응답, JSON 직렬화 등에 활용) ──
    print("\n" + "=" * 55)
    print("🔄 dataclass → dict 변환 (JSON 직렬화 준비)")
    print("=" * 55)
    
    from dataclasses import asdict
    
    sample = employees[0]
    sample_dict = asdict(sample)
    print(f"  원본 dataclass : {sample.name}, {sample.department}")
    print(f"  dict 변환 결과 : {sample_dict}")
    # → API 응답으로 보낼 때: json.dumps(asdict(employee))
    
    conn.close()
    print("\n✅ 완료")


if __name__ == "__main__":
    main()