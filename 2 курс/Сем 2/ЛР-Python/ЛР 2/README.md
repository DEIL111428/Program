# Лабораторная работа № 2

## Формулировка задания

1. Реализовать код с паттерном «Декоратор», который:
    - возвращал бы данные в формате json, yaml, csv;
    - использовался бы интерфейс (использовался ABC, @abstractmethod).
        
**Критерии:** Наличие тестов (unittest или pytest), докстринг (PEP-257), аннотация типов, оформление кода с использованием PEP-8.

## Описание работы кода

1. `DataComponent`
    - **Назначение**: базовый интерфейс (ABC) компонента для получения данных.
    - **Логика**: объявляет абстрактный метод `get_data()`.
        
2. `SimpleDataComponent(data: Dict[str, Any])`
    - **Назначение**: конкретный компонент, предоставляющий базовые данные.
    - **Параметры**: `data` (`Dict[str, Any]`) - данные для хранения и возврата.
    - **Логика**: при вызове `get_data()` возвращает сохраненный словарь с исходными данными.
        
3. `DataDecorator(component: DataComponent)`
    - **Назначение**: базовый класс декоратора.
    - **Параметры**: `component` (`DataComponent`) - оборачиваемый компонент источника данных.
    - **Логика**: реализует интерфейс `DataComponent` и делегирует получение данных обернутому компоненту.
        
4. `JSONFormatDecorator`, `YAMLFormatDecorator`, `CSVFormatDecorator`
    - **Назначение**: конкретные декораторы для форматирования данных.
    - **Логика**: получают исходные данные от базового компонента и возвращают их в виде отформатированной строки. В случае с `CSVFormatDecorator` дополнительно проверяется тип входных данных: если это не словарь, вызывается `TypeError`.
        

## Решение

```Python
"""
Модуль, реализующий паттерн «Декоратор» для форматирования данных.

Содержит абстрактный интерфейс источника данных и набор декораторов,
позволяющих преобразовывать базовые данные в форматы JSON, YAML и CSV
"""

import csv
import io
import json
import unittest
import yaml
from abc import ABC, abstractmethod
from typing import Any, Dict


class DataComponent(ABC):
    """Базовый интерфейс компонента для получения данных."""

    @abstractmethod
    def get_data(self) -> Any:
        """
        Возвращает данные.

        Returns:
            Any: Данные в произвольном формате (например, словарь).
        """
        pass


class SimpleDataComponent(DataComponent):
    """Конкретный компонент, предоставляющий базовые данные."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Инициализирует компонент с переданными данными.

        Args:
            data (Dict[str, Any]): Данные для хранения и возврата.
        """
        self._data = data

    def get_data(self) -> Dict[str, Any]:
        """
        Возвращает сохраненные данные.

        Returns:
            Dict[str, Any]: Словарь с исходными данными.
        """
        return self._data


class DataDecorator(DataComponent):
    """
    Базовый класс декоратора.

    Реализует тот же интерфейс, что и оборачиваемый компонент.
    """

    def __init__(self, component: DataComponent) -> None:
        """
        Инициализирует декоратор.

        Args:
            component (DataComponent): Оборачиваемый компонент источника данных.
        """
        self._component = component

    @abstractmethod
    def get_data(self) -> Any:
        """
        Делегирует получение данных обернутому компоненту.

        Returns:
            Any: Данные, полученные от базового компонента.
        """
        pass


class JSONFormatDecorator(DataDecorator):
    """Декоратор для преобразования данных в формат JSON."""

    def get_data(self) -> str:
        """
        Получает данные от базового компонента и возвращает их в JSON.

        Returns:
            str: Строка с данными в формате JSON.
        """
        data = self._component.get_data()
        return json.dumps(data, ensure_ascii=False, indent=4)


class YAMLFormatDecorator(DataDecorator):
    """Декоратор для преобразования данных в формат YAML."""

    def get_data(self) -> str:
        """
        Получает данные от базового компонента и возвращает их в YAML.

        Returns:
            str: Строка с данными в формате YAML.
        """
        data = self._component.get_data()
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)


class CSVFormatDecorator(DataDecorator):
    """Декоратор для преобразования данных в формат CSV."""

    def get_data(self) -> str:
        """
        Получает данные от базового компонента и возвращает их в CSV.

        Ожидается, что базовые данные представляют собой словарь.
        Ключи становятся первым столбцом, а значения - вторым.

        Returns:
            str: Строка с табличными данными в формате CSV.

        Raises:
            TypeError: Если данные не являются словарем.
        """
        data = self._component.get_data()
        
        if not isinstance(data, dict):
            raise TypeError("CSVFormatDecorator ожидает данные в виде словаря.")

        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["Key", "Value"])
        for key, value in data.items():
            writer.writerow([key, value])

        return output.getvalue()


class TestDataDecorators(unittest.TestCase):
    """Набор тестов для проверки работоспособности декораторов."""

    def setUp(self) -> None:
        """Подготовка тестовых данных перед каждым тестом."""
        self.raw_data = {"USD": 90.5, "EUR": 98.2}
        self.component = SimpleDataComponent(self.raw_data)

    def test_json_decorator(self) -> None:
        """Проверка корректной конвертации в формат JSON."""
        json_decorator = JSONFormatDecorator(self.component)
        result = json_decorator.get_data()
        
        self.assertIn('"USD": 90.5', result)
        self.assertIn('"EUR": 98.2', result)
        
        parsed_data = json.loads(result)
        self.assertEqual(parsed_data, self.raw_data)

    def test_yaml_decorator(self) -> None:
        """Проверка корректной конвертации в формат YAML."""
        yaml_decorator = YAMLFormatDecorator(self.component)
        result = yaml_decorator.get_data()
        
        self.assertIn('USD: 90.5', result)
        self.assertIn('EUR: 98.2', result)
        
        parsed_data = yaml.safe_load(result)
        self.assertEqual(parsed_data, self.raw_data)

    def test_csv_decorator(self) -> None:
        """Проверка корректной конвертации в формат CSV."""
        csv_decorator = CSVFormatDecorator(self.component)
        result = csv_decorator.get_data()
        
        self.assertIn('Key,Value', result)
        self.assertIn('USD,90.5', result)
        self.assertIn('EUR,98.2', result)

    def test_csv_decorator_type_error(self) -> None:
        """Проверка вызова исключения при неверном типе данных для CSV."""
        bad_component = SimpleDataComponent(["не", "словарь"]) 
        csv_decorator = CSVFormatDecorator(bad_component)
        
        with self.assertRaises(TypeError):
            csv_decorator.get_data()


if __name__ == "__main__":
    unittest.main()
```

## Проверка

Тесты реализованы с помощью встроенного модуля `unittest`. Проверяется корректность конвертации словаря в требуемые форматы, а также правильная обработка исключений.

#### Основные тест-кейсы:

- `test_json_decorator`: проверка корректной сериализации данных в формат JSON и возможность их обратного парсинга.
- `test_yaml_decorator`: проверка сериализации данных в формат YAML и их совпадения с исходным словарем при обратном чтении.
- `test_csv_decorator`: проверка наличия правильных заголовков столбцов и значений при конвертации данных в формат CSV.
- `test_csv_decorator_type_error`: проверка вызова исключения `TypeError` при попытке передать структуру данных, отличную от словаря, в CSV-декоратор.
    
## Информация о студенте
Иванов Федор Владиславович, 2 курс, ИВТ-1.2