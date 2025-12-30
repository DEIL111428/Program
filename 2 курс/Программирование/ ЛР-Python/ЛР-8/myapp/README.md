# Лабораторная работа № 8

## 1. Цель работы
Реализовать CRUD (Create, Read, Update, Delete) для сущностей бизнес-логики приложения. Освоить работу с SQLite в памяти (`:memory:`) через модуль `sqlite3`. Понять принципы первичных и внешних ключей и их роль в связях между таблицами. Выделить контроллеры для работы с БД и для рендеринга страниц в отдельные модули. Использовать архитектуру MVC и соблюдать разделение ответственности. Реализовать полноценный роутер, который обрабатывает GET-запросы и выполняет сохранение/обновление данных и рендеринг страниц. Научиться тестировать функционал на примере сущностей `currency` и `user` с использованием `unittest.mock`.

## 2. Описание предметной области

### Модели и их свойства

- **Author**
  - `name` - имя автора (str)
  - `group` - учебная группа (str)

- **App**
  - `name` - название приложения (str)
  - `version` - версия приложения (str)
  - `author` - объект Author

- **User**
  - `id` - уникальный идентификатор (int, PRIMARY KEY AUTOINCREMENT)
  - `name` - имя пользователя (str, NOT NULL)

- **Currency**
  - `id` - уникальный идентификатор (str, PRIMARY KEY, например R01235)
  - `num_code` - цифровой код ISO 4217 (str, например "840")
  - `char_code` - символьный код ISO 4217 (str, ровно 3 символа, например "USD")
  - `name` - название валюты (str)
  - `value` - курс в рублях (float, не может быть отрицательным)
  - `nominal` - номинал (int)

- **UserCurrency**
  - `id` - уникальный идентификатор (int)
  - `user_id` - внешний ключ на User (int, FOREIGN KEY)
  - `currency_id` - внешний ключ на Currency (str, FOREIGN KEY)
  - Связь many-to-many с ограничением UNIQUE(user_id, currency_id)

## 3. Структура проекта

```
myapp/
├── models/
│   ├── __init__.py
│   └── entities.py                # Модели (Author, App, User, Currency, UserCurrency)
├── controllers/
│   ├── __init__.py
│   ├── database_controller.py     # DatabaseController, UserCRUD, CurrencyCRUD, UserCurrencyCRUD
│   ├── currencies_controller.py   # CurrenciesController (бизнес-логика)
│   ├── users_controller.py        # UsersController (бизнес-логика)
│   └── pages_controller.py        # PagesController (рендеринг Jinja2)
├── templates/
│   ├── index.html                 # Главная страница
│   ├── users.html                 # Список пользователей
│   ├── user_detail.html           # Информация о пользователе и его подписки
│   └── currencies.html            # Список валют
├── utils/
│   ├── __init__.py
│   └── currencies_api.py          # Функция get_currencies для API ЦБ РФ
├── myapp.py                       # HTTP сервер, маршрутизация, инициализация
├── tests.py                       # Юнит-тесты с unittest.mock
└── README.md                      
```

## 4. Описание реализации

### Модели и их свойства

Все модели реализованы в `models/entities.py` с использованием properties, типов и валидацией:

```python
class Currency:
    def __init__(self, currency_id: str, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self._id = currency_id
        self._num_code = num_code
        self._char_code = char_code
        self._name = name
        self._value = value
        self._nominal = nominal
    
    @property
    def char_code(self) -> str:
        return self._char_code
    
    @char_code.setter
    def char_code(self, val: str) -> None:
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self._char_code = val.upper()
    
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, val: float) -> None:
        if val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self._value = val
```

### SQL таблицы и ключи

**Таблица user:**
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
```
- PRIMARY KEY гарантирует уникальность ID каждого пользователя
- AUTOINCREMENT автоматически увеличивает ID при добавлении записи

**Таблица currency:**
```sql
CREATE TABLE currency (
    id TEXT PRIMARY KEY,
    num_code TEXT NOT NULL,
    char_code TEXT NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    nominal INTEGER NOT NULL
);
```

**Таблица user_currency:**
```sql
CREATE TABLE user_currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    currency_id TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(currency_id) REFERENCES currency(id),
    UNIQUE(user_id, currency_id)
);
```
- Связь many-to-many между User и Currency
- FOREIGN KEY обеспечивает целостность данных
- UNIQUE гарантирует, что пользователь не может подписаться на одну валюту дважды

### CRUD операции

**DatabaseController** - управление подключением к SQLite:
```python
class DatabaseController:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self._create_tables()
```

**UserCRUD** - операции с пользователями:
```python
# Create
cursor.execute("INSERT INTO user(name) VALUES(?)", (name,))

# Read
cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))

# Update
cursor.execute("UPDATE user SET name = ? WHERE id = ?", (name, user_id))

# Delete
cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
```

**CurrencyCRUD** - операции с валютами (аналогично)

**UserCurrencyCRUD** - операции с подписками:
```python
# Добавить подписку
cursor.execute(
    "INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)",
    (user_id, currency_id)
)

# Получить подписки пользователя
cursor.execute(
    """SELECT c.* FROM currency c
       INNER JOIN user_currency uc ON c.id = uc.currency_id
       WHERE uc.user_id = ?""",
    (user_id,)
)
```

**Все SQL запросы параметризованы (?)** для защиты от SQL-инъекций.

### Контроллеры бизнес-логики

**CurrenciesController** - управление валютами:
- `get_all_currencies()` - получить все валюты
- `add_currency()` - добавить валюту
- `update_currency_value(currency_id, new_value)` - обновить курс
- `delete_currency(currency_id)` - удалить валюту
- `load_currencies_from_api(api_data)` - загрузить из API ЦБ РФ

**UsersController** - управление пользователями:
- `create_user(name)` - создать пользователя
- `get_all_users()` - получить всех пользователей
- `delete_user(user_id)` - удалить пользователя
- `subscribe_to_currency(user_id, currency_id)` - подписать на валюту
- `get_user_subscriptions(user_id)` - получить подписки пользователя

### Контроллер рендеринга

**PagesController** - рендеринг HTML через Jinja2:
```python
class PagesController:
    def __init__(self, env: Environment):
        self.env = env
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        template = self.env.get_template(template_name)
        return template.render(**context)
```

### Маршруты приложения

| Маршрут                             | Метод | Описание                  |
| ----------------------------------- | ----- | ------------------------- |
| `/`                                 | GET   | Главная страница          |
| `/users`                            | GET   | Список пользователей      |
| `/user?id=...`                      | GET   | Информация о пользователе |
| `/currencies`                       | GET   | Список валют              |
| `/currency/delete?id=...`           | GET   | Удаление валюты           |
| `/currency/update?id=...&value=...` | GET   | Обновление курса          |
| `/user/delete?id=...`               | GET   | Удаление пользователя     |
| `POST /users`                       | POST  | Создание пользователя     |
| `POST /subscribe`                   | POST  | Подписка на валюту        |

## 5. Примеры работы приложения

- Главная страница: `http://localhost:8000/`
[![image.png](https://i.postimg.cc/LXpxfdpX/image.png)](https://postimg.cc/XZsKSzXS)
- Список пользователей: `http://localhost:8000/users`
[![image.png](https://i.postimg.cc/rw4G9hgN/image.png)](https://postimg.cc/v4Q6YtJ4)
- Информация о пользователе: `http://localhost:8000/user?id=4`
[![image.png](https://i.postimg.cc/WzDq13HY/image.png)](https://postimg.cc/Fk4HP9m0)
- Список валют: `http://localhost:8000/currencies`
[![image.png](https://i.postimg.cc/pdqmQzN0/image.png)](https://postimg.cc/B8PZ48nD)
## 6. Тестирование

В `tests.py` используется `unittest.mock` для тестирования:

### Тесты моделей
```python
def test_currency_value_validation():
    """Проверка валидации курса валюты."""
    curr = Currency("R01", "840", "USD", "Dollar", 75.5, 1)
    with pytest.raises(ValueError):
        curr.value = -10.0
```

### Тесты контроллеров с mock
```python
class TestCurrenciesControllerWithMock(unittest.TestCase):
    def setUp(self):
        self.mock_crud = MagicMock(spec=CurrencyCRUD)
        self.controller = CurrenciesController(self.mock_crud)
    
    def test_get_all_currencies(self):
        mock_currencies = [
            {'id': 'R01235', 'char_code': 'USD', 'value': 75.5},
            {'id': 'R01239', 'char_code': 'EUR', 'value': 85.0}
        ]
        self.mock_crud.read_all.return_value = mock_currencies
        
        result = self.controller.get_all_currencies()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['char_code'], 'USD')
        self.mock_crud.read_all.assert_called_once()
```

### Запуск тестов
```bash
python -m unittest tests.py -v
```
[![image.png](https://i.postimg.cc/mgV9j0C6/image.png)](https://postimg.cc/nXjMcSdv)

## 7. Ключевые концепции

### PRIMARY KEY и FOREIGN KEY

**PRIMARY KEY** - уникально идентифицирует каждую запись в таблице. Гарантирует:
- Нет дублирования
- Быстрый поиск по ID
- Целостность данных

**FOREIGN KEY** - ссылается на PRIMARY KEY другой таблицы. Гарантирует:
- Целостность данных между связанными таблицами
- Невозможно добавить подписку с несуществующим пользователем
- Каскадное удаление при удалении пользователя

### MVC архитектура

- **Model** (`entities.py`) - классы данных с валидацией
- **View** (`templates/*.html`) - HTML шаблоны Jinja2
- **Controller** (`controllers/` и `myapp.py`) - бизнес-логика и маршрутизация

### Защита от SQL-инъекций

Все SQL запросы используют параметризованный формат:
```python
# Безопасно
cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))

# Небезопасно 
cursor.execute(f"SELECT * FROM user WHERE id = '{user_id}'")
```

## 8. Выводы

- ✅ Реализованы полные CRUD операции для всех сущностей
- ✅ SQLite база данных в памяти с поддержкой PRIMARY и FOREIGN KEY
- ✅ Архитектура MVC с четким разделением ответственности
- ✅ Все SQL запросы параметризованы для безопасности
- ✅ HTTP маршрутизация для GET и POST запросов
- ✅ Код документирован согласно PEP 257
- ✅ Тесты с использованием `unittest.mock`

---

**Запуск приложения:**
```bash
python myapp/myapp.py
# Сервер запустится на http://localhost:8000/
```

**Запуск тестов:**
```bash
python -m unittest tests.py -v
```

## Информация о студенте
Иванов ФВ, 2 курс, ИВТ-1.2