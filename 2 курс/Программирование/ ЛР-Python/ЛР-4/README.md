# Лабораторная работа № 4

## Формулировка задания
Разработайте программу на языке Python, которая будет строить **бинарное дерево** (_дерево, в каждом узле которого может быть только два потомка_). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева. 

**Необходимо реализовать нерекурсивный вариант gen_bin_tree**  

Алгоритм построения дерева должен учитывать параметры, переданные в качестве аргументов функции. Пример:   

```Python
def gen_bin_tree(height=<number>, root=<number>, left_branch=lambda l_r: l_r, right_branch=lambda r_r: r_r):**

    pass
```

Если параметры были переданы, то используются они. В противном случае используются параметры, указанные в варианте.

Root = 8; height = 4, 
left_leaf = root+root/2, right_leaf = root^2

## Описание работы кода
1. gen_bin_tree(height=4, root=8)
	- Это рекурсивная функция, которая создаёт **бинарное дерево**.
		Параметры
		- height - сколько уровней дерева ещё нужно сгенерировать.
		- root - значение текущего узла (корня дерева на этом уровне).
		База рекурсии:
		- Если height == 0, возвращаем None. Это значит, что на этом уровне дерева узлов нет.
		Генерация значений дочерних узлов:
		- left_leaf = root + root / 2 - значение левого ребёнка.
		- right_leaf = root ** 2 - значение правого ребёнка.
	    Генерация значений дочерних узлов:
	    - left_leaf = root + root / 2 - значение левого ребёнка.
	    - right_leaf = root ** 2 - значение правого ребёнка.
		Возврат словаря:
		- Узел представлен как словарь:
			``` python
			{
			  'value': root,
			  'left': левое_поддерево,
			  'right': правое_поддерево
			}

			```
2. Функция bfs_lvl (обход в ширину)
	- Это обход дерева в ширину (Breadth-First Search, BFS) с разделением узлов по уровням.
	- Используется очередь (queue), чтобы хранить узлы, которые нужно обработать.
		На каждом шаге:
		-  level_size = len(queue) - сколько узлов на текущем уровне.
		- for i in range(level_size) - обрабатываем только текущий уровень.
		- pop(0) - достаём узел из начала очереди.
		- Добавляем его значение в current_level.
		- Если есть левый или правый ребёнок, добавляем их в очередь, чтобы обработать на следующем уровне.
	- После обработки всех узлов текущего уровня, добавляем current_level в levels.
	- В итоге levels - список списков, где каждый вложенный список содержит значения узлов на одном уровне.
3. Генерация дерева и вывод уровней
	- gen_bin_tree(4, 8) создаёт дерево высотой 4 с корнем 8.
	- bfs_lvl(tree) собирает узлы по уровням.
	- Выводит каждый уровень отдельно.
## Решение
```Python
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
        tree = gen_bin_tree(height=2, root_value=8)
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

    # Дополнительный тест: проверка с кастомными функциями
    def test_custom_branches(self):
        tree = gen_bin_tree(
            height=2,
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


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
```
## Информация о студенте
Иванов ФВ, 2 курс, ИВТ-1.2