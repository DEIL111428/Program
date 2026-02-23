import unittest
from models.entities import User, Currency

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

if __name__ == '__main__':
    unittest.main()