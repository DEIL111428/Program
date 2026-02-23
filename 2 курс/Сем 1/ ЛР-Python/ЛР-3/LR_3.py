import json
from typing import Callable, Dict, Optional

def gen_bin_tree(
    height: int = 4,
    root_value: float = 8,
    left_branch: Callable = lambda x: x + x/2,
    right_branch: Callable = lambda x: x ** 2
) -> Optional[Dict]:
    """Генерирует бинарное дерево заданной высоты с корневым значением.

    Функция рекурсивно строит бинарное дерево, где каждое значение узла
    определяется применением заданных функций к значению родительского узла:
    - левый потомок вычисляется через `left_branch`,
    - правый потомок — через `right_branch`.

    Аргументы:
        height (int): Высота дерева. Высота 0 соответствует дереву из одного узла.
                      Если `height < 0`, функция возвращает `None`.
        root_value (float): Начальное значение корневого узла.
        left_branch (Callable[[float], float]): Функция для вычисления значения
                                                левого потомка.
        right_branch (Callable[[float], float]): Функция для вычисления значения
                                                 правого потомка.

    Возвращает:
        Optional[Dict]: Представление дерева в виде вложенного словаря с ключами
                        'value', 'left' и 'right'. Если `height < 0`, возвращается `None`.
                        
    Пример:
        >>> tree = gen_bin_tree(height=2, root_value=1)
        >>> print(json.dumps(tree, indent=2))
        {
          "value": 1,
          "left": {
            "value": 1.5,
            "left": {"value": 2.25, "left": null, "right": null},
            "right": {"value": 2.25, "left": null, "right": null}
          },
          "right": {
            "value": 1,
            "left": {"value": 1.5, "left": null, "right": null},
            "right": {"value": 1, "left": null, "right": null}
          }
        }
    """

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

