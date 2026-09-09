import time
import threading


def calculate_a():
    result = 0

    for i in range(100_000_000):
        result += i * i

    return result


def calculate_b():
    result = 0

    for i in range(100_000_000):
        result += i * i

    return result


# Thread에서 결과를 저장할 변수
result_a = 0
result_b = 0


def run_a():
    global result_a
    result_a = calculate_a()


def run_b():
    global result_b
    result_b = calculate_b()


# 시작 시간
start = time.perf_counter()

# Thread 생성
thread_a = threading.Thread(target=run_a)
thread_b = threading.Thread(target=run_b)

# Thread 시작
thread_a.start()
thread_b.start()

# 두 Thread가 끝날 때까지 대기
thread_a.join()
thread_b.join()

# 결과 합산
total = result_a + result_b

# 종료 시간
end = time.perf_counter()

print(f"Result A : {result_a}")
print(f"Result B : {result_b}")
print(f"Total    : {total}")
print(f"Elapsed  : {end - start:.2f} seconds")

'''
Elapsed  : 3.81 seconds
'''
