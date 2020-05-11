from concurrent.futures import ThreadPoolExecutor


def f(x):
    return x * x


with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(f, 12)
    print(future.result())
