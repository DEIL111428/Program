from collections import deque

def gen_bin_tree(height=3, root_value=8, left_branch=lambda l_r: l_r + l_r / 2, right_branch=lambda r_r: r_r**2):
    if height <= 0:
        return None

    root = {'value': root_value, 'left': None, 'right': None}
    if height == 1:
        return root

    queue = deque([root])  # Очередь для обхода дерева в ширину

    for _ in range(1, height): 
        for _ in range(len(queue)):
            node = queue.popleft()

            # Создаём левое поддерево
            left_val =  left_branch(node['value'])
            node['left'] = {'value': left_val, 'left': None, 'right': None}
            queue.append(node['left'])

            # Создаём правое поддерево
            right_val = right_branch(node['value'])
            node['right'] = {'value': right_val, 'left': None, 'right': None}
            queue.append(node['right'])

    return root

def print_tree(tree, otstup=0):
    if tree is None:
        return None
    print_tree(tree['right'], otstup + 4)
    print(' ' * otstup + f"{tree['value']}")
    print_tree(tree['left'], otstup + 4)

if __name__ == "__main__":
    tree = gen_bin_tree(4, 8)
    print_tree(tree)

