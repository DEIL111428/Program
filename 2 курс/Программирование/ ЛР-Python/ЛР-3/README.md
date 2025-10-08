# Лабораторная работа № 3

## Формулировка задания
Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева.

Root = 8; height = 4, 
left_leaf = root+root/2, right_leaf = root^2

## Описание работы кода
1. gen_bin_tree(height=4, root=8)

	- Назначение: рекурсивно строит полный бинарный дерево в виде вложенных словарей.
	- Вход:
		- height - сколько уровней ещё создать (целое). При height == 0 возвращает None (лист отсутствует).
		- root - значение текущего узла (может стать float при делении)
	- Логика:
	    - Если height == 0 → return None.
	    - Вычисляет значения потомков:
	        - left_leaf = root + root / 2
	        - right_leaf = root ** 2
    - Возвращает словарь: {'value': root, 'left': gen_bin_tree(height-1, left_leaf), 'right': gen_bin_tree(height-1, right_leaf)}.
	- Результат: дерево, где у каждого узла ключи 'value', 'left', 'right'. Общее число узлов ≈ 2^height − 1.
2. print_tree(tree, otstup=0)
    
    - Назначение: печатает дерево "повёрнутым" на 90° (правые ветви сверху, левые - снизу).
    - Вход:
        - tree - узел (словарь) или None.
        - otstup - текущий отступ в пробелах (уровень * 4).
    - Логика:
        - Если tree is None → return (ничего не печатается) - это базовый случай рекурсии и защита от обращения к None.
        - Сначала рекурсивно печатает правое поддерево с otstup+4 (будет выше).
        - Затем печатает значение текущего узла с otstup пробелами.
        - Затем рекурсивно печатает левое поддерево с otstup+4 (будет ниже).
    - Итог: визуализация с отступами, где вертикальное положение соответствует правым/левым ветвям.
3. Конец файла
	- tree = gen_bin_tree() - создаёт дерево с параметрами по умолчанию.
	- print_tree(tree) - выводит дерево в консоль.
## Решение
```Python
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
```
## Проверка
- Импортируется функция gen_bin_tree.
- Создаётся класс TestBinaryTree.
- В классе определены 8 тестовых методов, каждый проверяет работу функции на разных входных данных. В каждом из методов создаём дерево: tree = gen_bin_tree(height=3, root=8):
	- test_tree_1: проверяет, что для tree\['value'] возвращается 8.
	- test_tree_2: проверяет, что для tree\['left']\['value'] возвращается 12.0.
	- test_tree_3: проверяет, что для \['right']\['value'] возвращается 64.
- В конце запускается тестовый раннер с помощью unittest.main(), чтобы выполнить тесты и вывести подробный результат.
```Python
import unittest
from LR_3 import gen_bin_tree
class TestBinaryTree(unittest.TestCase):
    def test_tree_1(self):
        tree = gen_bin_tree(height=3, root=8)
        self.assertEqual(tree['value'], 8)
        
    def test_tree_2(self):
        tree = gen_bin_tree(height=3, root=8)
        self.assertEqual(tree['left']['value'], 12.0)

    def test_tree_3(self):
        tree = gen_bin_tree(height=3, root=8)
        self.assertEqual(tree['right']['value'], 64)

    def test_tree_4(self):
        tree = gen_bin_tree(height=3, root=8)
        self.assertEqual(tree['left']['left']['value'], 18.0)
    
    def test_tree_5(self):
        tree = gen_bin_tree(height=3, root=8)
        self.assertEqual(tree['left']['right']['value'], 144.0)
    
    def test_tree_6(self):
        tree = gen_bin_tree(height=3, root=8)
        self.assertEqual(tree['right']['left']['value'], 96.0)
    
    def test_tree_7(self):
        tree = gen_bin_tree(height=3, root=8)
        self.assertEqual(tree['right']['right']['value'], 4096)

    def test_tree_values(self):
        tree = gen_bin_tree(height=2, root=8)
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
    

unittest.main(argv=[''], verbosity=2, exit=False)
```