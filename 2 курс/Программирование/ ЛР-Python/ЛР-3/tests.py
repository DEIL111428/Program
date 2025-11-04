import unittest
from LR_3 import gen_bin_tree


class TestBinaryTree(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_zero_height_tree(self):
        expected = {'value': 8, 'left': None, 'right': None}
        result = gen_bin_tree(height=0, root_value=8)
        self.assertEqual(result, expected)

    def test_default_tree_height_two(self):
        expected = {
            'value': 8,
            'left': {
                'value': 12.0,
                'left': None,
                'right': None
            },
            'right': {
                'value': 64,
                'left': None,
                'right': None
            }
        }
        result = gen_bin_tree(height=1, root_value=8)
        self.assertEqual(result, expected)

    def test_custom_functions(self):
        expected = {
            'value': 2,
            'left': {
                'value': 3,
                'left': None,
                'right': None
            },
            'right': {
                'value': 6,
                'left': None,
                'right': None
            }
        }
        result = gen_bin_tree(
            height=1,
            root_value=2,
            left_branch=lambda x: x + 1,
            right_branch=lambda x: x * 3
        )
        self.assertEqual(result, expected)

    def test_negative_height(self):
        result = gen_bin_tree(height=-1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
