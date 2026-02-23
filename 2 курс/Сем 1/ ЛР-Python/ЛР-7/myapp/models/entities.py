"""
Модуль содержит модели предметной области приложения.

Соответствует слою Model в архитектуре MVC.
"""


class Author:
    """
    Класс, описывающий автора приложения.
    """

    def __init__(self, name: str, group: str) -> None:
        """
        Инициализация автора.

        Args:
            name (str): Имя автора.
            group (str): Группа.
        """
        self._name = name
        self._group = group

    @property
    def name(self) -> str:
        """Возвращает имя автора."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает имя автора. Должно быть строкой."""
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        self._name = value

    @property
    def group(self) -> str:
        """Возвращает группу автора."""
        return self._group


class App:
    """
    Класс, описывающий приложение.
    """

    def __init__(self, name: str, version: str, author: Author) -> None:
        """
        Инициализация приложения.

        Args:
            name (str): Название приложения.
            version (str): Версия приложения.
            author (Author): Объект автора.
        """
        self._name = name
        self._version = version
        self._author = author

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def author(self) -> Author:
        return self._author


class User:
    """
    Класс пользователя.
    """

    def __init__(self, user_id: int, name: str) -> None:
        """
        Инициализация пользователя.

        Args:
            user_id (int): Уникальный ID.
            name (str): Имя пользователя.
        """
        self._id = user_id
        self.name = name  # Используем сеттер для валидации

    @property
    def id(self) -> int:
        """Возвращает ID пользователя."""
        return self._id

    @property
    def name(self) -> str:
        """Возвращает имя пользователя."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Устанавливает имя пользователя.

        Args:
            value (str): Новое имя.

        Raises:
            ValueError: Если имя пустое.
        """
        if not value or not isinstance(value, str):
            raise ValueError("Имя пользователя не может быть пустым")
        self._name = value


class Currency:
    """
    Класс валюты.
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
        Инициализация валюты.

        Args:
            curr_id (str): ID валюты (например, R01235).
            num_code (str): Цифровой код ISO.
            char_code (str): Символьный код ISO.
            name (str): Название валюты.
            value (float): Текущий курс.
            nominal (int): Номинал.
        """
        self._id = curr_id
        self._num_code = num_code
        self._char_code = char_code
        self._name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> str:
        return self._id

    @property
    def char_code(self) -> str:
        return self._char_code

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, val: float) -> None:
        """Устанавливает курс. Должен быть положительным."""
        if val < 0:
            raise ValueError("Курс не может быть отрицательным")
        self._value = val

    @property
    def nominal(self) -> int:
        return self._nominal

    @nominal.setter
    def nominal(self, val: int) -> None:
        if val <= 0:
            raise ValueError("Номинал должен быть больше 0")
        self._nominal = val


class UserCurrency:
    """
    Связующая сущность для подписки пользователя на валюту.
    """

    def __init__(self, uc_id: int, user_id: int, currency_id: str) -> None:
        """
        Инициализация связи.

        Args:
            uc_id (int): Уникальный ID записи.
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.
        """
        self._id = uc_id
        self._user_id = user_id
        self._currency_id = currency_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def currency_id(self) -> str:
        return self._currency_id