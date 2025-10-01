import unittest
from LR_2 import sum_of_two

class TestMath(unittest.TestCase):
    def test_sum_of_two_1(self):
        self.assertEqual(sum_of_two([2, 7, 11, 15], 9), [0, 1])
        
    def test_sum_of_two_2(self):
        self.assertEqual(sum_of_two([3, 2, 4], 6), [1, 2])

    def test_sum_of_two_3(self):
        self.assertEqual(sum_of_two([3, 3], 6), [0, 1])

    def test_sum_of_two_no_result(self):
        self.assertEqual(sum_of_two([1, 2, 3], 10), [])

    def test_sum_of_two_negative_numbers(self):
        self.assertEqual(sum_of_two([-1, -2, -3, 4], 1), [2, 3])

    def test_sum_of_two_duplicates(self):
        self.assertEqual(sum_of_two([1, 2, 2, 3], 4), [0, 3])

unittest.main(argv=[''], verbosity=2, exit=False)
