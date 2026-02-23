# LR_5.py
import timeit
import matplotlib.pyplot as plt
from functools import lru_cache


def fact_recursive(n: int) -> int:
    """
    Вычисляет факториал числа n рекурсивным способом без мемоизации.

    Аргументы:
        n (int): Неотрицательное целое число, для которого вычисляется факториал.

    Возвращает:
        int: Факториал числа n.

    Примеры:
        >>> fact_recursive(0)
        1
        >>> fact_recursive(1)
        1
        >>> fact_recursive(5)
        120
    """
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """
    Вычисляет факториал числа n итеративным способом без мемоизации.

    Аргументы:
        n (int): Неотрицательное целое число, для которого вычисляется факториал.

    Возвращает:
        int: Факториал числа n.

    Примеры:
        >>> fact_iterative(0)
        1
        >>> fact_iterative(4)
        24
        >>> fact_iterative(6)
        720
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@lru_cache(maxsize=None)
def fact_recursive_memo(n: int) -> int:
    """
    Вычисляет факториал числа n рекурсивным способом с мемоизацией через functools.lru_cache.

    Аргументы:
        n (int): Неотрицательное целое число, для которого вычисляется факториал.

    Возвращает:
        int: Факториал числа n.
    
    Примеры:
        >>> fact_recursive_memo(0)
        1
        >>> fact_recursive_memo(3)
        6
        >>> fact_recursive_memo(7)
        5040
    """
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive_memo(n - 1)


def fact_iterative_memo(n: int, cache: dict = {}) -> int:
    """
    Вычисляет факториал числа n итеративным способом с ручной мемоизацией через словарь.

    Аргументы:
        n (int): Неотрицательное целое число, для которого вычисляется факториал.
        cache (dict): Кэш для хранения ранее вычисленных значений (по умолчанию пустой словарь).

    Возвращает:
        int: Факториал числа n.

    Примеры:
        >>> fact_iterative_memo(0)
        1
        >>> fact_iterative_memo(5)
        120
        >>> cache = {}
        >>> fact_iterative_memo(4, cache=cache)
        24
        >>> fact_iterative_memo(5, cache=cache)  # использует результат для 4
        120
    """
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


def benchmark(func, n: int) -> float:
    """
    Измеряет время выполнения функции func при вычислении факториала числа n.

    Аргументы:
        func (callable): Функция для измерения времени выполнения.
        n (int): Аргумент, передаваемый в функцию func.

    Возвращает:
        float: Время выполнения функции в секундах (один прогон).
    """
    stmt = lambda: func(n)
    t = timeit.timeit(stmt, number=1)
    return t


# Глобальные параметры для бенчмарка
numbers = list(range(5, 501, 25))
repeat_count = 5

# Сравнение производительности
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


# Визуализация результатов
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
