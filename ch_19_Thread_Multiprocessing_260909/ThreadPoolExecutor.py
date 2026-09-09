from concurrent.futures import ThreadPoolExecutor
import time


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


start = time.perf_counter()

with ThreadPoolExecutor(max_workers=2) as executor:

    future_a = executor.submit(calculate_a)
    future_b = executor.submit(calculate_b)

    result_a = future_a.result()
    result_b = future_b.result()


total = result_a + result_b

end = time.perf_counter()

print(f"Result A : {result_a}")
print(f"Result B : {result_b}")
print(f"Total    : {total}")
print(f"Elapsed  : {end - start:.2f} seconds")

# Elapsed  : 3.66 seconds