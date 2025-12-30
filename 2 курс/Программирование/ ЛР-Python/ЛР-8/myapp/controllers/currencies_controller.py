"""
Модуль контроллера валют.

Содержит бизнес-логику для работы с валютами приложения.
Использует CurrencyCRUD для работы с базой данных.

Классы:
    - CurrenciesController: контроллер валют
"""

from typing import List, Dict, Any, Optional
from controllers.database_controller import CurrencyCRUD, DatabaseController


class CurrenciesController:
    """
    Контроллер валют приложения.

    Предоставляет методы для управления валютами на уровне бизнес-логики.
    Использует CurrencyCRUD для работы с БД.

    Атрибуты:
        crud (CurrencyCRUD): CRUD контроллер для работы с валютами.
    """

    def __init__(self, crud: CurrencyCRUD) -> None:
        """
        Инициализирует контроллер валют.

        Args:
            crud (CurrencyCRUD): CRUD операции для валют.
        """
        self.crud = crud

    def add_currency(
        self,
        curr_id: str,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int
    ) -> str:
        """
        Добавляет новую валюту в систему.

        Args:
            curr_id (str): Уникальный ID валюты.
            num_code (str): Цифровой код ISO.
            char_code (str): Символьный код ISO (3 символа).
            name (str): Название валюты.
            value (float): Текущий курс.
            nominal (int): Номинал.

        Returns:
            str: ID добавленной валюты.

        Raises:
            ValueError: Если данные некорректны.
        """
        return self.crud.create(curr_id, num_code, char_code, name, value, nominal)

    def get_currency(self, currency_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о валюте по ID.

        Args:
            currency_id (str): ID валюты.

        Returns:
            Optional[Dict[str, Any]]: Данные валюты или None.
        """
        return self.crud.read(currency_id)

    def get_all_currencies(self) -> List[Dict[str, Any]]:
        """
        Получает список всех доступных валют.

        Returns:
            List[Dict[str, Any]]: Список валют.
        """
        return self.crud.read_all()

    def get_currency_by_code(self, char_code: str) -> Optional[Dict[str, Any]]:
        """
        Получает валюту по символьному коду (USD, EUR и т.д.).

        Args:
            char_code (str): Символьный код валюты.

        Returns:
            Optional[Dict[str, Any]]: Данные валюты или None.
        """
        return self.crud.read_by_char_code(char_code)

    def update_currency_value(self, currency_id: str, new_value: float) -> bool:
        """
        Обновляет курс валюты.

        Args:
            currency_id (str): ID валюты.
            new_value (float): Новый курс.

        Returns:
            bool: True если обновление успешно, False если валюта не найдена.

        Raises:
            ValueError: Если курс отрицательный.
        """
        return self.crud.update(currency_id, new_value)

    def delete_currency(self, currency_id: str) -> bool:
        """
        Удаляет валюту из системы.

        Все подписки пользователей на эту валюту также удаляются.

        Args:
            currency_id (str): ID валюты для удаления.

        Returns:
            bool: True если валюта удалена, False если не найдена.
        """
        return self.crud.delete(currency_id)

    def load_currencies_from_api(
        self,
        currencies_data: List[Dict[str, Any]]
    ) -> int:
        """
        Загружает валюты из API ЦБ РФ в БД.

        Args:
            currencies_data (List[Dict[str, Any]]): Список валют из API.

        Returns:
            int: Количество загруженных валют.
        """
        count = 0
        for item in currencies_data:
            try:
                self.add_currency(
                    curr_id=item.get('id', ''),
                    num_code=item.get('num_code', ''),
                    char_code=item.get('char_code', ''),
                    name=item.get('name', ''),
                    value=item.get('value', 0.0),
                    nominal=item.get('nominal', 1)
                )
                count += 1
            except (ValueError, KeyError):
                # Пропускаем некорректные записи
                continue
        return count
