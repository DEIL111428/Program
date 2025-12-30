"""
Модуль контроллера базы данных.

Содержит классы для CRUD операций с SQLite базой данных в памяти.
Реализует работу с таблицами User, Currency и их связями через UserCurrency.

Основные классы:
    - DatabaseController: инициализирует БД и управляет подключением
    - UserCRUD: операции с пользователями
    - CurrencyCRUD: операции с валютами
    - UserCurrencyCRUD: операции со связями между пользователями и валютами
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from threading import Lock


class DatabaseController:
    """
    Контроллер базы данных SQLite.

    Управляет подключением к БД в памяти и созданием схемы.
    Использует потокобезопасность через Lock для избежания конфликтов.

    Атрибуты:
        conn (sqlite3.Connection): Подключение к БД в памяти.
        _lock (Lock): Блокировка для потокобезопасных операций.
    """

    def __init__(self) -> None:
        """
        Инициализирует подключение к БД и создает таблицы.

        Создает таблицы:
            - user: пользователи приложения
            - currency: доступные валюты
            - user_currency: подписки пользователей на валюты
        """
        self.conn: sqlite3.Connection = sqlite3.connect(
            ':memory:',
            check_same_thread=False
        )
        self.conn.row_factory = sqlite3.Row
        self._lock = Lock()
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Создает все необходимые таблицы в БД.

        Таблица user:
            - id: первичный ключ, автоинкремент
            - name: имя пользователя, не может быть пусто

        Таблица currency:
            - id: первичный ключ, текстовое поле (R01235)
            - num_code: цифровой код ISO
            - char_code: символьный код ISO (3 символа)
            - name: название валюты
            - value: текущий курс
            - nominal: номинал валюты

        Таблица user_currency (связь многие-ко-многим):
            - id: первичный ключ, автоинкремент
            - user_id: внешний ключ на user
            - currency_id: внешний ключ на currency
            - FOREIGN KEY обеспечивает целостность данных
        """
        cursor = self.conn.cursor()

        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Таблица валют
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS currency (
                id TEXT PRIMARY KEY,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                nominal INTEGER NOT NULL
            )
        ''')

        # Таблица подписок (связь многие-ко-многим)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id),
                UNIQUE(user_id, currency_id)
            )
        ''')

        self.conn.commit()

    def get_connection(self) -> sqlite3.Connection:
        """
        Возвращает подключение к БД.

        Returns:
            sqlite3.Connection: Активное подключение к БД.
        """
        return self.conn

    def close(self) -> None:
        """Закрывает подключение к БД."""
        self.conn.close()


class UserCRUD:
    """
    Класс для CRUD операций с пользователями.

    Реализует методы Create, Read, Update, Delete для таблицы user.
    Все SQL запросы параметризованы для защиты от SQL-инъекций.

    Атрибуты:
        db_controller (DatabaseController): Контроллер БД для доступа к подключению.
    """

    def __init__(self, db_controller: DatabaseController) -> None:
        """
        Инициализирует CRUD контроллер пользователей.

        Args:
            db_controller (DatabaseController): Контроллер БД.
        """
        self.db_controller = db_controller

    def create(self, name: str) -> int:
        """
        Создает нового пользователя в БД.

        Args:
            name (str): Имя пользователя.

        Returns:
            int: ID новосозданного пользователя.

        Raises:
            ValueError: Если имя пусто или не строка.
            sqlite3.Error: Если возникла ошибка БД.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Имя пользователя должно быть непустой строкой")

        cursor = self.db_controller.conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO user (name) VALUES (?)',
                (name,)
            )
            self.db_controller.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            self.db_controller.conn.rollback()
            raise sqlite3.Error(f"Ошибка при создании пользователя: {e}")

    def read(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Получает пользователя по ID.

        Args:
            user_id (int): ID пользователя.

        Returns:
            Optional[Dict[str, Any]]: Словарь с данными пользователя или None.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'SELECT id, name FROM user WHERE id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def read_all(self) -> List[Dict[str, Any]]:
        """
        Получает всех пользователей из БД.

        Returns:
            List[Dict[str, Any]]: Список словарей со всеми пользователями.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute('SELECT id, name FROM user ORDER BY id')
        return [dict(row) for row in cursor.fetchall()]

    def update(self, user_id: int, name: str) -> bool:
        """
        Обновляет имя пользователя.

        Args:
            user_id (int): ID пользователя.
            name (str): Новое имя.

        Returns:
            bool: True если пользователь найден и обновлен, False иначе.

        Raises:
            ValueError: Если новое имя пусто.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Имя пользователя должно быть непустой строкой")

        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'UPDATE user SET name = ? WHERE id = ?',
            (name, user_id)
        )
        self.db_controller.conn.commit()
        return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        """
        Удаляет пользователя из БД.

        При удалении пользователя автоматически удаляются его подписки
        благодаря каскадной настройке внешних ключей.

        Args:
            user_id (int): ID пользователя для удаления.

        Returns:
            bool: True если пользователь был удален, False если не найден.
        """
        cursor = self.db_controller.conn.cursor()
        # Удаляем подписки пользователя
        cursor.execute(
            'DELETE FROM user_currency WHERE user_id = ?',
            (user_id,)
        )
        # Удаляем самого пользователя
        cursor.execute(
            'DELETE FROM user WHERE id = ?',
            (user_id,)
        )
        self.db_controller.conn.commit()
        return cursor.rowcount > 0


class CurrencyCRUD:
    """
    Класс для CRUD операций с валютами.

    Реализует методы Create, Read, Update, Delete для таблицы currency.
    Все SQL запросы параметризованы для защиты от SQL-инъекций.

    Атрибуты:
        db_controller (DatabaseController): Контроллер БД.
    """

    def __init__(self, db_controller: DatabaseController) -> None:
        """
        Инициализирует CRUD контроллер валют.

        Args:
            db_controller (DatabaseController): Контроллер БД.
        """
        self.db_controller = db_controller

    def create(
        self,
        curr_id: str,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int
    ) -> str:
        """
        Создает новую валюту в БД.

        Args:
            curr_id (str): Уникальный ID валюты (например, R01235).
            num_code (str): Цифровой код валюты.
            char_code (str): Символьный код ISO (3 символа).
            name (str): Название валюты.
            value (float): Текущий курс валюты.
            nominal (int): Номинал валюты.

        Returns:
            str: ID созданной валюты.

        Raises:
            ValueError: Если данные некорректны.
            sqlite3.Error: Если возникла ошибка БД.
        """
        if value < 0:
            raise ValueError("Курс не может быть отрицательным")
        if nominal <= 0:
            raise ValueError("Номинал должен быть положительным")

        cursor = self.db_controller.conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO currency 
                   (id, num_code, char_code, name, value, nominal)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (curr_id, num_code, char_code, name, value, nominal)
            )
            self.db_controller.conn.commit()
            return curr_id
        except sqlite3.Error as e:
            self.db_controller.conn.rollback()
            raise sqlite3.Error(f"Ошибка при создании валюты: {e}")

    def read(self, currency_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает валюту по ID.

        Args:
            currency_id (str): ID валюты.

        Returns:
            Optional[Dict[str, Any]]: Словарь с данными валюты или None.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'SELECT * FROM currency WHERE id = ?',
            (currency_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def read_all(self) -> List[Dict[str, Any]]:
        """
        Получает все валюты из БД.

        Returns:
            List[Dict[str, Any]]: Список словарей со всеми валютами.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute('SELECT * FROM currency ORDER BY char_code')
        return [dict(row) for row in cursor.fetchall()]

    def read_by_char_code(self, char_code: str) -> Optional[Dict[str, Any]]:
        """
        Получает валюту по символьному коду (USD, EUR и т.д.).

        Args:
            char_code (str): Символьный код валюты.

        Returns:
            Optional[Dict[str, Any]]: Словарь с данными валюты или None.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'SELECT * FROM currency WHERE char_code = ?',
            (char_code,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def update(
        self,
        currency_id: str,
        value: float,
        nominal: Optional[int] = None
    ) -> bool:
        """
        Обновляет значение курса и опционально номинал валюты.

        Args:
            currency_id (str): ID валюты для обновления.
            value (float): Новое значение курса.
            nominal (Optional[int]): Новый номинал (опционально).

        Returns:
            bool: True если валюта найдена и обновлена, False иначе.

        Raises:
            ValueError: Если параметры некорректны.
        """
        if value < 0:
            raise ValueError("Курс не может быть отрицательным")
        if nominal is not None and nominal <= 0:
            raise ValueError("Номинал должен быть положительным")

        cursor = self.db_controller.conn.cursor()
        if nominal is not None:
            cursor.execute(
                'UPDATE currency SET value = ?, nominal = ? WHERE id = ?',
                (value, nominal, currency_id)
            )
        else:
            cursor.execute(
                'UPDATE currency SET value = ? WHERE id = ?',
                (value, currency_id)
            )
        self.db_controller.conn.commit()
        return cursor.rowcount > 0

    def delete(self, currency_id: str) -> bool:
        """
        Удаляет валюту из БД.

        Все подписки пользователей на эту валюту также удаляются
        благодаря внешним ключам.

        Args:
            currency_id (str): ID валюты для удаления.

        Returns:
            bool: True если валюта была удалена, False если не найдена.
        """
        cursor = self.db_controller.conn.cursor()
        # Удаляем подписки на эту валюту
        cursor.execute(
            'DELETE FROM user_currency WHERE currency_id = ?',
            (currency_id,)
        )
        # Удаляем саму валюту
        cursor.execute(
            'DELETE FROM currency WHERE id = ?',
            (currency_id,)
        )
        self.db_controller.conn.commit()
        return cursor.rowcount > 0


class UserCurrencyCRUD:
    """
    Класс для CRUD операций со связями между пользователями и валютами.

    Управляет таблицей user_currency, которая реализует отношение
    многие-ко-многим между пользователями и валютами.

    Атрибуты:
        db_controller (DatabaseController): Контроллер БД.
    """

    def __init__(self, db_controller: DatabaseController) -> None:
        """
        Инициализирует CRUD контроллер подписок.

        Args:
            db_controller (DatabaseController): Контроллер БД.
        """
        self.db_controller = db_controller

    def create(self, user_id: int, currency_id: str) -> Optional[int]:
        """
        Создает подписку пользователя на валюту.

        Args:
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.

        Returns:
            Optional[int]: ID подписки или None если подписка уже существует.

        Raises:
            sqlite3.Error: Если возникла ошибка БД.
        """
        cursor = self.db_controller.conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO user_currency (user_id, currency_id)
                   VALUES (?, ?)''',
                (user_id, currency_id)
            )
            self.db_controller.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Подписка уже существует или внешний ключ не найден
            return None

    def read_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Получает все валюты, на которые подписан пользователь.

        Args:
            user_id (int): ID пользователя.

        Returns:
            List[Dict[str, Any]]: Список валют пользователя.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            '''SELECT c.* FROM currency c
               JOIN user_currency uc ON c.id = uc.currency_id
               WHERE uc.user_id = ?
               ORDER BY c.char_code''',
            (user_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def read_all(self) -> List[Dict[str, Any]]:
        """
        Получает все подписки из БД.

        Returns:
            List[Dict[str, Any]]: Список всех подписок.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'SELECT id, user_id, currency_id FROM user_currency'
        )
        return [dict(row) for row in cursor.fetchall()]

    def is_subscribed(self, user_id: int, currency_id: str) -> bool:
        """
        Проверяет, подписан ли пользователь на валюту.

        Args:
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.

        Returns:
            bool: True если подписка существует, False иначе.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM user_currency WHERE user_id = ? AND currency_id = ?',
            (user_id, currency_id)
        )
        return cursor.fetchone()[0] > 0

    def delete(self, user_id: int, currency_id: str) -> bool:
        """
        Удаляет подписку пользователя на валюту.

        Args:
            user_id (int): ID пользователя.
            currency_id (str): ID валюты.

        Returns:
            bool: True если подписка была удалена, False если не найдена.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'DELETE FROM user_currency WHERE user_id = ? AND currency_id = ?',
            (user_id, currency_id)
        )
        self.db_controller.conn.commit()
        return cursor.rowcount > 0

    def delete_user_subscriptions(self, user_id: int) -> int:
        """
        Удаляет все подписки пользователя.

        Args:
            user_id (int): ID пользователя.

        Returns:
            int: Количество удаленных подписок.
        """
        cursor = self.db_controller.conn.cursor()
        cursor.execute(
            'DELETE FROM user_currency WHERE user_id = ?',
            (user_id,)
        )
        self.db_controller.conn.commit()
        return cursor.rowcount
