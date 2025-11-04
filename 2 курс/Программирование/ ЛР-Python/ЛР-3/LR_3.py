import json
from typing import Callable, Dict, Optional

def gen_bin_tree(
    height: int = 4,
    root_value: float = 8,
    left_branch: Callable = lambda x: x + x/2,
    right_branch: Callable = lambda x: x ** 2
) -> Optional[Dict]:
    
    if height < 0:
        return None

    tree = {
        'value': root_value,
        'left': None,
        'right': None
    }

    if height > 0:
        left_value = left_branch(root_value)
        right_value = right_branch(root_value)
        
        tree['left'] = gen_bin_tree(height - 1, left_value, left_branch, right_branch)
        tree['right'] = gen_bin_tree(height - 1, right_value, left_branch, right_branch)

    return tree

def print_tree(tree: Dict) -> None:
    print(json.dumps(tree, indent=4))

if __name__ == "__main__":
    tree = gen_bin_tree(height=4)
    print_tree(tree)
