# LR_5.py
import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# 1. Реализации факториала

def fact_recursive(n):
    """Рекурсивный вариант без мемоизации"""
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive(n - 1)

def fact_iterative(n):
    """Итеративный вариант без мемоизации"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

@lru_cache(maxsize=None)
def fact_recursive_memo(n):
    """Рекурсивный вариант с мемоизацией"""
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive_memo(n - 1)


def fact_iterative_memo(n, cache={}):
    """Итеративный вариант с мемоизацией"""
    if n in cache:
        return cache[n]
    result = 1
    for i in range(2, n + 1):
        if i in cache:
            result = cache[i]
        else:
            result *= i
            cache[i] = result
    return result





numbers = list(range(5, 501, 25))  
repeat_count = 5  

def benchmark(func, n):
    """Измеряет среднее время выполнения функции для одного числа n"""
    stmt = lambda: func(n)
    t = timeit.timeit(stmt, number=1)
    return t


# 3. Сравнение


results_recursive = []
results_iterative = []
results_recursive_memo = []
results_iterative_memo = []

for n in numbers:
    t1 = min(timeit.repeat(lambda: fact_recursive(n), repeat=repeat_count, number=1))
    t2 = min(timeit.repeat(lambda: fact_iterative(n), repeat=repeat_count, number=1))
    t3 = min(timeit.repeat(lambda: fact_recursive_memo(n), repeat=repeat_count, number=1))
    t4 = min(timeit.repeat(lambda: fact_iterative_memo(n), repeat=repeat_count, number=1))

    results_recursive.append(t1)
    results_iterative.append(t2)
    results_recursive_memo.append(t3)
    results_iterative_memo.append(t4)


# 4. Визуализация


plt.figure(figsize=(10, 6))
plt.plot(numbers, results_recursive, 'r-o', label="Рекурсивный")
plt.plot(numbers, results_iterative, 'b-o', label="Итеративный")
plt.plot(numbers, results_recursive_memo, 'g--o', label="Рекурсивный (мемо)")
plt.plot(numbers, results_iterative_memo, 'm--o', label="Итеративный (мемо)")
plt.xlabel("n")
plt.ylabel("Время выполнения (сек.)")
plt.title("Сравнение времени выполнения факториала")
plt.legend()
plt.grid(True)
plt.show()


