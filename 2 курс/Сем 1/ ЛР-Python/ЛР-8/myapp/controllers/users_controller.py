"""
Модуль контроллера пользователей.

Содержит бизнес-логику для работы с пользователями приложения.
Использует UserCRUD для работы с базой данных.

Классы:
    - UsersController: контроллер пользователей
"""

from typing import List, Dict, Any, Optional
from controllers.database_controller import UserCRUD, UserCurrencyCRUD, DatabaseController


class UsersController:
    """
    Контроллер пользователей приложения.

    Предоставляет методы для управления пользователями и их подписками.
    Использует UserCRUD и UserCurrencyCRUD для работы с БД.

    Атрибуты:
        user_crud (UserCRUD): CRUD операции для пользователей.
        user_currency_crud (UserCurrencyCRUD): CRUD операции для подписок.
    """

    def __init__(
        self,
        user_crud: UserCRUD,
        user_currency_crud: UserCurrencyCRUD
    ) -> None:
        """
        Инициализирует контроллер пользователей.

        Args:
            user_crud (UserCRUD): CRUD операции для пользователей.
            user_currency_crud (UserCurrencyCRUD): CRUD операции для подписок.
        """
        self.user_crud = user_crud
        self.user_currency_crud = user_currency_crud

    def create_user(self, name: str) -> int:
        """
        Создает нового пользователя.

        Args:
            name (str): Имя пользователя.

        Returns:
            int: ID созданного пользователя.

        Raises:
            ValueError: Если имя некорректно.
        """
        return self.user_crud.create(name)

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о пользователе.

        Args:
            user_id (int): ID пользователя.

        Returns:
            Optional[Dict[str, Any]]: Данные пользователя или None.
        """
        return self.user_crud.read(user_id)

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Получает список всех пользователей.

        Returns:
            List[Dict[str, Any]]: Список пользователей.
        """
        return self.user_crud.read_all()

    def update_user(self, user_id: int, name: str) -> bool:
        """
        Обновляет имя пользователя.

        Args:
            user_id (int): ID пользователя.
            name (str): Новое имя.

        Returns:
            bool: True если обновление успешно, False если пользователь не найден.

        Raises:
            ValueError: Если имя некорректно.
        """
        return self.user_crud.update(user_id, name)

    def delete_user(self, user_id: int) -> bool:
        """
        Удаляет пользователя из системы.

        Все подписки пользователя также удаляются.

        Args:
            user_id (int): ID пользователя для удаления.

        Returns:
            bool: True если пользователь удален, False если не найден.
        """
        return self.user_crud.delete(user_id)

    def subscribe_to_currency(self, user_id: int, currency_id: str) -> bool:
        """
        Подписывает пользователя на валюту.

        Args:
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.

        Returns:
            bool: True если подписка создана, False если уже подписан или ошибка.
        """
        result = self.user_currency_crud.create(user_id, currency_id)
        return result is not None

    def unsubscribe_from_currency(self, user_id: int, currency_id: str) -> bool:
        """
        Отписывает пользователя от валюты.

        Args:
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.

        Returns:
            bool: True если подписка удалена, False если не найдена.
        """
        return self.user_currency_crud.delete(user_id, currency_id)

    def is_subscribed(self, user_id: int, currency_id: str) -> bool:
        """
        Проверяет, подписан ли пользователь на валюту.

        Args:
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.

        Returns:
            bool: True если подписан, False иначе.
        """
        return self.user_currency_crud.is_subscribed(user_id, currency_id)

    def get_user_subscriptions(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Получает список валют, на которые подписан пользователь.

        Args:
            user_id (int): ID пользователя.

        Returns:
            List[Dict[str, Any]]: Список валют пользователя.
        """
        return self.user_currency_crud.read_user_currencies(user_id)
