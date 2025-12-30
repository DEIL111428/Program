import unittest
from unittest.mock import MagicMock, patch

# Импорты моделей
from models.entities import User, Currency

# Импорты контроллеров
from controllers.database_controller import (
    DatabaseController,
    UserCRUD,
    CurrencyCRUD,
    UserCurrencyCRUD
)
from controllers.currencies_controller import CurrenciesController
from controllers.users_controller import UsersController


# ===========================
# ТЕСТЫ МОДЕЛЕЙ
# ===========================

class TestModels(unittest.TestCase):
    """
    Тестирование моделей данных.
    """

    def test_user_creation(self):
        """Проверка создания пользователя и геттеров."""
        user = User(1, "TestName")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "TestName")

    def test_user_validation(self):
        """Проверка валидации имени пользователя."""
        user = User(1, "Valid")
        with self.assertRaises(ValueError):
            user.name = ""  # Пустое имя

    def test_currency_creation(self):
        """Проверка создания валюты."""
        curr = Currency("R01", "840", "USD", "Dollar", 75.5, 1)
        self.assertEqual(curr.char_code, "USD")
        self.assertEqual(curr.value, 75.5)

    def test_currency_value_validation(self):
        """Проверка, что курс не может быть отрицательным."""
        curr = Currency("R01", "840", "USD", "Dollar", 75.5, 1)
        with self.assertRaises(ValueError):
            curr.value = -10.0


# ===========================
# ТЕСТЫ КОНТРОЛЛЕРОВ С МОКАМИ
# ===========================

class TestCurrenciesControllerWithMock(unittest.TestCase):
    """Тестирование CurrenciesController с использованием моков."""

    def setUp(self) -> None:
        """Создание mock объектов для тестирования."""
        self.mock_crud = MagicMock(spec=CurrencyCRUD)
        self.controller = CurrenciesController(self.mock_crud)

    def test_get_all_currencies(self) -> None:
        """Тестирование получения всех валют."""
        mock_currencies = [
            {'id': 'R01235', 'char_code': 'USD', 'value': 75.5},
            {'id': 'R01239', 'char_code': 'EUR', 'value': 85.0}
        ]
        self.mock_crud.read_all.return_value = mock_currencies

        result = self.controller.get_all_currencies()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['char_code'], 'USD')
        self.mock_crud.read_all.assert_called_once()

    def test_get_currency_by_code(self) -> None:
        """Тестирование получения валюты по коду."""
        mock_currency = {'id': 'R01235', 'char_code': 'USD', 'value': 75.5}
        self.mock_crud.read_by_char_code.return_value = mock_currency

        result = self.controller.get_currency_by_code("USD")

        self.assertEqual(result['char_code'], 'USD')
        self.mock_crud.read_by_char_code.assert_called_once_with("USD")

    def test_update_currency_value(self) -> None:
        """Тестирование обновления курса валюты."""
        self.mock_crud.update.return_value = True

        result = self.controller.update_currency_value("R01235", 80.0)

        self.assertTrue(result)
        self.mock_crud.update.assert_called_once_with("R01235", 80.0)

    def test_delete_currency(self) -> None:
        """Тестирование удаления валюты."""
        self.mock_crud.delete.return_value = True

        result = self.controller.delete_currency("R01235")

        self.assertTrue(result)
        self.mock_crud.delete.assert_called_once_with("R01235")


class TestUsersControllerWithMock(unittest.TestCase):
    """Тестирование UsersController с использованием моков."""

    def setUp(self) -> None:
        """Создание mock объектов для тестирования."""
        self.mock_user_crud = MagicMock(spec=UserCRUD)
        self.mock_uc_crud = MagicMock(spec=UserCurrencyCRUD)
        self.controller = UsersController(self.mock_user_crud, self.mock_uc_crud)

    def test_get_all_users(self) -> None:
        """Тестирование получения всех пользователей."""
        mock_users = [
            {'id': 1, 'name': 'Алексей'},
            {'id': 2, 'name': 'Мария'}
        ]
        self.mock_user_crud.read_all.return_value = mock_users

        result = self.controller.get_all_users()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Алексей')
        self.mock_user_crud.read_all.assert_called_once()

    def test_get_user(self) -> None:
        """Тестирование получения пользователя."""
        mock_user = {'id': 1, 'name': 'Алексей'}
        self.mock_user_crud.read.return_value = mock_user

        result = self.controller.get_user(1)

        self.assertEqual(result['name'], 'Алексей')
        self.mock_user_crud.read.assert_called_once_with(1)

    def test_subscribe_to_currency(self) -> None:
        """Тестирование подписки на валюту."""
        self.mock_uc_crud.create.return_value = 1

        result = self.controller.subscribe_to_currency(1, "R01235")

        self.assertTrue(result)
        self.mock_uc_crud.create.assert_called_once_with(1, "R01235")

    def test_is_subscribed(self) -> None:
        """Тестирование проверки подписки."""
        self.mock_uc_crud.is_subscribed.return_value = True

        result = self.controller.is_subscribed(1, "R01235")

        self.assertTrue(result)
        self.mock_uc_crud.is_subscribed.assert_called_once_with(1, "R01235")

    def test_get_user_subscriptions(self) -> None:
        """Тестирование получения подписок пользователя."""
        mock_currencies = [
            {'id': 'R01235', 'char_code': 'USD'},
            {'id': 'R01239', 'char_code': 'EUR'}
        ]
        self.mock_uc_crud.read_user_currencies.return_value = mock_currencies

        result = self.controller.get_user_subscriptions(1)

        self.assertEqual(len(result), 2)
        self.mock_uc_crud.read_user_currencies.assert_called_once_with(1)



if __name__ == '__main__':
    unittest.main()
