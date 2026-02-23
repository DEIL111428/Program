from collections import deque

def gen_bin_tree(height=3, root_value=8, left_branch=lambda l_r: l_r + l_r / 2, right_branch=lambda r_r: r_r**2):
    """
    Генерирует бинарное дерево заданной высоты с корневым значением и заданными функциями для левой и правой ветвей.

    Высота дерева определяется как количество уровней:
      - height = 0 → только корень (1 узел)
      - height = 1 → корень + его непосредственные дети (3 узла)
      - height = n → n+1 уровень узлов

    Аргументы:
        height (int): Высота дерева (должна быть >= 0). По умолчанию 3.
        root_value (float или int): Значение корневого узла. По умолчанию 8.
        left_branch (callable): Функция, вычисляющая значение левого потомка из родительского значения.
                                По умолчанию: lambda x: x + x / 2.
        right_branch (callable): Функция, вычисляющая значение правого потомка из родительского значения.
                                 По умолчанию: lambda x: x ** 2.

    Возвращает:
        dict или None: Словарь, представляющий корень дерева, с ключами 'value', 'left', 'right'.
                       Возвращает None только если height < 0.

    Пример:
        >>> tree = gen_bin_tree(height=0, root_value=5)
        >>> tree == {'value': 5, 'left': None, 'right': None}
        True
    """
    if height < 0: 
        return None

    root = {'value': root_value, 'left': None, 'right': None}
    if height == 0:
        return root

    queue = deque([root]) # Очередь для обхода дерева в ширину

    for _ in range(1, height + 1):
        for _ in range(len(queue)):
            node = queue.popleft()

            # Создаём левое поддерево
            left_val = left_branch(node['value'])
            node['left'] = {'value': left_val, 'left': None, 'right': None}
            queue.append(node['left'])

            # Создаём правое поддерево
            right_val = right_branch(node['value'])
            node['right'] = {'value': right_val, 'left': None, 'right': None}
            queue.append(node['right'])

    return root


def print_tree(tree, otstup=0):
    """Рекурсивно выводит дерево в виде перевёрнутого (право-корень-лево) ASCII-дерева."""
    if tree is None:
        return
    print_tree(tree['right'], otstup + 4)
    print(' ' * otstup + f"{tree['value']}")
    print_tree(tree['left'], otstup + 4)


if __name__ == "__main__":
    tree = gen_bin_tree(4, 8)
    print_tree(tree)
