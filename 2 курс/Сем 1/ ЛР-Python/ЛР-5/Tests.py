# tests.py
import unittest
from LR_5 import fact_recursive, fact_iterative, fact_recursive_memo, fact_iterative_memo
import math


class TestFactorials(unittest.TestCase):

    def test_small_numbers(self):
        """Проверка факториала для малых чисел"""
        for n in range(6):  # от 0 до 5
            expected = math.factorial(n)
            self.assertEqual(fact_recursive(n), expected)
            self.assertEqual(fact_iterative(n), expected)
            self.assertEqual(fact_recursive_memo(n), expected)
            self.assertEqual(fact_iterative_memo(n), expected)

    def test_larger_numbers(self):
        """Проверка факториала для больших чисел"""
        for n in [10, 20, 30]:
            expected = math.factorial(n)
            self.assertEqual(fact_recursive(n), expected)
            self.assertEqual(fact_iterative(n), expected)
            self.assertEqual(fact_recursive_memo(n), expected)
            self.assertEqual(fact_iterative_memo(n), expected)

    def test_zero(self):
        """Проверка базового случая 0! = 1"""
        self.assertEqual(fact_recursive(0), 1)
        self.assertEqual(fact_iterative(0), 1)
        self.assertEqual(fact_recursive_memo(0), 1)
        self.assertEqual(fact_iterative_memo(0), 1)



if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
