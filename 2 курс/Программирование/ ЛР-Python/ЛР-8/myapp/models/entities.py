"""
Модуль моделей предметной области приложения.

Содержит классы для представления основных сущностей приложения:
    - Author: информация об авторе приложения
    - App: метаинформация о приложении
    - User: пользователь системы
    - Currency: валюта
    - UserCurrency: подписка пользователя на валюту

Соответствует слою Model в архитектуре MVC.
Используются properties для инкапсуляции и валидации данных.
"""

from typing import Optional


class Author:
    """
    Модель автора приложения.

    Содержит информацию об авторе (имя, группа).
    Используется для отображения информации в интерфейсе.

    Атрибуты:
        _name (str): Приватное имя автора.
        _group (str): Приватная группа автора.
    """

    def __init__(self, name: str, group: str) -> None:
        """
        Инициализирует объект автора.

        Args:
            name (str): Имя автора.
            group (str): Группа (например, ИВТ-1.2).

        Raises:
            TypeError: Если параметры не строки.
        """
        if not isinstance(name, str) or not isinstance(group, str):
            raise TypeError("Имя и группа должны быть строками")
        self._name = name
        self._group = group

    @property
    def name(self) -> str:
        """
        Возвращает имя автора.

        Returns:
            str: Имя автора.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает имя автора.

        Args:
            value (str): Новое имя.

        Raises:
            TypeError: Если значение не строка.
        """
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        self._name = value

    @property
    def group(self) -> str:
        """
        Возвращает группу автора.

        Returns:
            str: Группа автора.
        """
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        """
        Устанавливает группу автора.

        Args:
            value (str): Новая группа.

        Raises:
            TypeError: Если значение не строка.
        """
        if not isinstance(value, str):
            raise TypeError("Группа должна быть строкой")
        self._group = value


class App:
    """
    Модель информации о приложении.

    Содержит метаинформацию: название, версию и информацию об авторе.
    Используется для отображения в интерфейсе.

    Атрибуты:
        _name (str): Приватное название приложения.
        _version (str): Приватная версия приложения.
        _author (Author): Приватный объект автора.
    """

    def __init__(self, name: str, version: str, author: Author) -> None:
        """
        Инициализирует объект приложения.

        Args:
            name (str): Название приложения.
            version (str): Версия приложения.
            author (Author): Объект автора.

        Raises:
            TypeError: Если параметры имеют неверный тип.
        """
        if not isinstance(name, str):
            raise TypeError("Название должно быть строкой")
        if not isinstance(version, str):
            raise TypeError("Версия должна быть строкой")
        if not isinstance(author, Author):
            raise TypeError("Автор должен быть объектом Author")

        self._name = name
        self._version = version
        self._author = author

    @property
    def name(self) -> str:
        """
        Возвращает название приложения.

        Returns:
            str: Название приложения.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает название приложения.

        Args:
            value (str): Новое название.

        Raises:
            TypeError: Если значение не строка.
        """
        if not isinstance(value, str):
            raise TypeError("Название должно быть строкой")
        self._name = value

    @property
    def version(self) -> str:
        """
        Возвращает версию приложения.

        Returns:
            str: Версия приложения.
        """
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        """
        Устанавливает версию приложения.

        Args:
            value (str): Новая версия.

        Raises:
            TypeError: Если значение не строка.
        """
        if not isinstance(value, str):
            raise TypeError("Версия должна быть строкой")
        self._version = value

    @property
    def author(self) -> Author:
        """
        Возвращает объект автора.

        Returns:
            Author: Объект автора приложения.
        """
        return self._author

    @author.setter
    def author(self, value: Author) -> None:
        """
        Устанавливает объект автора.

        Args:
            value (Author): Новый объект автора.

        Raises:
            TypeError: Если значение не объект Author.
        """
        if not isinstance(value, Author):
            raise TypeError("Автор должен быть объектом Author")
        self._author = value


class User:
    """
    Модель пользователя приложения.

    Представляет пользователя системы с ID и именем.
    ID генерируется БД автоматически при создании.

    Атрибуты:
        _id (int): Уникальный ID пользователя (первичный ключ).
        _name (str): Приватное имя пользователя.
    """

    def __init__(self, user_id: int, name: str) -> None:
        """
        Инициализирует объект пользователя.

        Args:
            user_id (int): Уникальный ID пользователя.
            name (str): Имя пользователя.

        Raises:
            TypeError: Если ID не целое число или имя не строка.
            ValueError: Если имя пусто.
        """
        if not isinstance(user_id, int):
            raise TypeError("ID должно быть целым числом")
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой")
        if not name or name.isspace():
            raise ValueError("Имя пользователя не может быть пустым")

        self._id = user_id
        self._name = name

    @property
    def id(self) -> int:
        """
        Возвращает ID пользователя.

        Returns:
            int: ID пользователя (не изменяется).
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Возвращает имя пользователя.

        Returns:
            str: Имя пользователя.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает имя пользователя.

        Args:
            value (str): Новое имя.

        Raises:
            TypeError: Если значение не строка.
            ValueError: Если имя пусто.
        """
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        if not value or value.isspace():
            raise ValueError("Имя пользователя не может быть пустым")
        self._name = value


class Currency:
    """
    Модель валюты.

    Представляет валюту с кодами (числовой и символьный), названием,
    текущим курсом и номиналом.

    Валидация:
        - Курс не может быть отрицательным
        - Номинал должен быть положительным

    Атрибуты:
        _id (str): Приватный ID валюты (первичный ключ из API).
        _num_code (str): Приватный цифровой код ISO.
        _char_code (str): Приватный символьный код ISO (3 символа).
        _name (str): Приватное название валюты.
        _value (float): Приватный текущий курс валюты.
        _nominal (int): Приватный номинал валюты.
    """

    def __init__(
        self,
        curr_id: str,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int
    ) -> None:
        """
        Инициализирует объект валюты.

        Args:
            curr_id (str): ID валюты (например, R01235).
            num_code (str): Цифровой код ISO (например, 840).
            char_code (str): Символьный код ISO (например, USD).
            name (str): Название валюты (например, Доллар США).
            value (float): Текущий курс валюты.
            nominal (int): Номинал валюты.

        Raises:
            TypeError: Если параметры имеют неверный тип.
            ValueError: Если значения некорректны.
        """
        if not isinstance(curr_id, str):
            raise TypeError("ID валюты должно быть строкой")
        if not isinstance(num_code, str):
            raise TypeError("Цифровой код должен быть строкой")
        if not isinstance(char_code, str):
            raise TypeError("Символьный код должен быть строкой")
        if not isinstance(name, str):
            raise TypeError("Название должно быть строкой")
        if not isinstance(value, (int, float)):
            raise TypeError("Курс должен быть числом")
        if not isinstance(nominal, int):
            raise TypeError("Номинал должен быть целым числом")

        if value < 0:
            raise ValueError("Курс не может быть отрицательным")
        if nominal <= 0:
            raise ValueError("Номинал должен быть положительным")

        self._id = curr_id
        self._num_code = num_code
        self._char_code = char_code
        self._name = name
        self._value = float(value)
        self._nominal = nominal

    @property
    def id(self) -> str:
        """
        Возвращает ID валюты.

        Returns:
            str: ID валюты (не изменяется).
        """
        return self._id

    @property
    def num_code(self) -> str:
        """
        Возвращает цифровой код ISO.

        Returns:
            str: Цифровой код валюты.
        """
        return self._num_code

    @property
    def char_code(self) -> str:
        """
        Возвращает символьный код ISO.

        Returns:
            str: Символьный код валюты (3 символа).
        """
        return self._char_code

    @property
    def name(self) -> str:
        """
        Возвращает название валюты.

        Returns:
            str: Название валюты.
        """
        return self._name

    @property
    def value(self) -> float:
        """
        Возвращает текущий курс валюты.

        Returns:
            float: Курс валюты.
        """
        return self._value

    @value.setter
    def value(self, val: float) -> None:
        """
        Устанавливает курс валюты.

        Args:
            val (float): Новый курс.

        Raises:
            TypeError: Если значение не число.
            ValueError: Если курс отрицательный.
        """
        if not isinstance(val, (int, float)):
            raise TypeError("Курс должен быть числом")
        if val < 0:
            raise ValueError("Курс не может быть отрицательным")
        self._value = float(val)

    @property
    def nominal(self) -> int:
        """
        Возвращает номинал валюты.

        Returns:
            int: Номинал валюты.
        """
        return self._nominal

    @nominal.setter
    def nominal(self, val: int) -> None:
        """
        Устанавливает номинал валюты.

        Args:
            val (int): Новый номинал.

        Raises:
            TypeError: Если значение не целое число.
            ValueError: Если номинал не положительный.
        """
        if not isinstance(val, int):
            raise TypeError("Номинал должен быть целым числом")
        if val <= 0:
            raise ValueError("Номинал должен быть положительным")
        self._nominal = val


class UserCurrency:
    """
    Модель связи между пользователем и валютой.

    Реализует отношение многие-ко-многим между пользователями и валютами.
    Представляет подписку пользователя на определенную валюту.

    Атрибуты:
        _id (int): Уникальный ID подписки.
        _user_id (int): Внешний ключ на таблицу user.
        _currency_id (str): Внешний ключ на таблицу currency.
    """

    def __init__(self, uc_id: int, user_id: int, currency_id: str) -> None:
        """
        Инициализирует подписку пользователя на валюту.

        Args:
            uc_id (int): Уникальный ID подписки.
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.

        Raises:
            TypeError: Если параметры имеют неверный тип.
        """
        if not isinstance(uc_id, int):
            raise TypeError("ID подписки должно быть целым числом")
        if not isinstance(user_id, int):
            raise TypeError("ID пользователя должно быть целым числом")
        if not isinstance(currency_id, str):
            raise TypeError("ID валюты должно быть строкой")

        self._id = uc_id
        self._user_id = user_id
        self._currency_id = currency_id

    @property
    def id(self) -> int:
        """
        Возвращает ID подписки.

        Returns:
            int: ID подписки.
        """
        return self._id

    @property
    def user_id(self) -> int:
        """
        Возвращает ID пользователя.

        Returns:
            int: ID пользователя.
        """
        return self._user_id

    @property
    def currency_id(self) -> str:
        """
        Возвращает ID валюты.

        Returns:
            str: ID валюты.
        """
        return self._currency_id
