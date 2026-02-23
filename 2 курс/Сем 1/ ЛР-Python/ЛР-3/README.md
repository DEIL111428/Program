# Лабораторная работа № 3

## Формулировка задания
Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева.

Root = 8; height = 4, 
left_leaf = root+root/2, right_leaf = root^2

## Описание работы кода
1. gen_bin_tree(height=4, root_value=8, left_branch=..., right_branch=...)

	- **Назначение**: рекурсивно строит полное бинарное дерево заданной высоты в виде вложенных словарей.
	- **Параметры**:
	    - height (int): высота дерева.
	        - При height = 0 возвращается узел без потомков (листья).
	        - При height < 0 возвращается None.
	    - root_value (float или Any): значение в корне текущего поддерева.
	    - left_branch (Callable): функция для вычисления значения левого потомка.
	    - right_branch (Callable): функция для вычисления значения правого потомка.
	- **Логика**:
	    - Если height < 0 → возвращает None.
	    - Создаёт узел с ключами 'value', 'left', 'right'.
	    - Если height > 0, рекурсивно строит левое и правое поддеревья с высотой height - 1.
2. print_tree(tree)

    - - **Назначение**: красивая печать дерева в консоль в формате JSON с отступами.
	- **Параметры**:
	    - tree (dict или None): сгенерированное дерево.
	- **Особенность**: использует json.dumps(tree, indent=4) для наглядного иерархического вывода, что упрощает отладку и проверку структуры.

## Решение
```Python
# LR_3.py

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
"""
```
## Проверка
Тесты реализованы с помощью модуля unittest. Проверяется **полная структура дерева**, а не отдельные узлы.

#### Основные тест-кейсы:

- test_zero_height_tree: дерево высоты 0 содержит только корень.
- test_default_tree_height_two: проверка структуры дерева высоты 1 с функциями по умолчанию.
- test_custom_functions: проверка работы с пользовательскими функциями вычисления потомков.
- test_negative_height: при отрицательной высоте возвращается None.

```Python
# tests.py

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
```
# Информация о студенте
Иванов Федор Владиславович, 2 курс, ИВТ-1.2
