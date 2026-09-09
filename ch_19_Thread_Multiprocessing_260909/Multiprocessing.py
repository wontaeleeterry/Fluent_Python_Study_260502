import time
import multiprocessing


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


if __name__ == "__main__":

    # 시작 시간
    start = time.perf_counter()

    # Process 생성
    process_a = multiprocessing.Process(
        target=calculate_a
    )

    process_b = multiprocessing.Process(
        target=calculate_b
    )

    # Process 시작
    process_a.start()
    process_b.start()

    # Process 종료까지 대기
    process_a.join()
    process_b.join()

    # 종료 시간
    end = time.perf_counter()

    print(f"Elapsed : {end - start:.2f} seconds")

''' 
Elapsed : 2.01 seconds
'''
