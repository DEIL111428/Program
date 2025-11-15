import unittest
from LR_4 import gen_bin_tree

class TestBinaryTree(unittest.TestCase):

    def test_tree_1(self):
        tree = gen_bin_tree(height=3, root_value=8)
        self.assertEqual(tree['value'], 8)

    def test_tree_2(self):
        tree = gen_bin_tree(height=3, root_value=8)
        self.assertEqual(tree['left']['value'], 12.0)

    def test_tree_3(self):
        tree = gen_bin_tree(height=3, root_value=8)
        self.assertEqual(tree['right']['value'], 64)

    def test_tree_4(self):
        tree = gen_bin_tree(height=3, root_value=8)
        self.assertEqual(tree['left']['left']['value'], 18.0)

    def test_tree_5(self):
        tree = gen_bin_tree(height=3, root_value=8)
        self.assertEqual(tree['left']['right']['value'], 144.0)

    def test_tree_6(self):
        tree = gen_bin_tree(height=3, root_value=8)
        self.assertEqual(tree['right']['left']['value'], 96.0)

    def test_tree_7(self):
        tree = gen_bin_tree(height=3, root_value=8)
        self.assertEqual(tree['right']['right']['value'], 4096)

    def test_tree_values(self):
        tree = gen_bin_tree(height=1, root_value=8)
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
        self.assertEqual(tree, expected)

    def test_custom_branches(self):
        tree = gen_bin_tree(
            height=1,
            root_value=2,
            left_branch=lambda x: x + 1,
            right_branch=lambda x: x * 3
        )
        expected = {
            'value': 2,
            'left': {'value': 3, 'left': None, 'right': None},
            'right': {'value': 6, 'left': None, 'right': None}
        }
        self.assertEqual(tree, expected)

    def test_height_zero(self):
        tree = gen_bin_tree(height=0, root_value=5)
        expected = {'value': 5, 'left': None, 'right': None}
        self.assertEqual(tree, expected)

    def test_negative_height(self):
        tree = gen_bin_tree(height=-1, root_value=5)
        self.assertIsNone(tree)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
