def gen_bin_tree(height=4, root=8):
    if height == 0:
        return None
    left_leaf = root + root / 2
    right_leaf = root ** 2
    return {
        'value': root,
        'left': gen_bin_tree(height - 1, left_leaf),
        'right': gen_bin_tree(height - 1, right_leaf)
    }

def print_tree(tree, otstup=0):
    if tree is None:
        return None
    print_tree(tree['right'], otstup + 4)
    print(' ' * otstup + f"{tree['value']}")
    print_tree(tree['left'], otstup + 4)

if __name__ == "__main__":
    tree = gen_bin_tree()
    print_tree(tree)

"""
            16777216
        4096
            6144.0
    64
            9216.0
        96.0
            144.0
8
            20736.0
        144.0
            216.0
    12.0
            324.0
        18.0
            27.0
"""



