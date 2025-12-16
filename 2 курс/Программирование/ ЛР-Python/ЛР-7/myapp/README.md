# Лабораторная работа № 7

## 1. Цель работы
Краткая цель: создать простое клиент‑серверное приложение на Python без сторонних серверных фреймворков, освоить работу с `HTTPServer` и маршрутизацию, применить шаблонизатор Jinja2 для отображения данных, реализовать модели предметной области (`User`, `Currency`, `UserCurrency`, `App`, `Author`) с геттерами/сеттерами, интегрировать получение курсов валют через функцию `get_currencies`, организовать архитектуру в стиле MVC и написать тесты для моделей и логики.

## 2. Описание предметной области
Модели и их свойства:

- `Author`
  - `name` - имя автора
  - `group` - учебная группа

- `App`
  - `name` - название приложения
  - `version` - версия приложения
  - `author` - объект `Author`

- `User`
  - `id` - уникальный идентификатор (int)
  - `name` - имя пользователя (str)

- `Currency`
  - `id` - уникальный идентификатор (str)
  - `num_code` - цифровой код (str|int)
  - `char_code` - символьный код (str)
  - `name` - название валюты (str)
  - `value` - курс (float)
  - `nominal` - номинал (int)

- `UserCurrency`
  - `id` - уникальный идентификатор
  - `user_id` - внешний ключ к `User`
  - `currency_id` - внешний ключ к `Currency`

Связи: `User` и `Currency` связаны через `UserCurrency` (many-to-many).

Пример XML-формата валюты (источник API):

```
<Valute ID="R01280">
 <NumCode>360</NumCode>
 <CharCode>IDR</CharCode>
 <Nominal>10000</Nominal>
 <Name>Рупий</Name>
 <Value>48,6178</Value>
</Valute>
```

## 3. Структура проекта
Рекомендуемая и текущая структура:

```
myapp/
├── models/
│   └── entities.py            # все модели 
├── templates/
│   ├── index.html
│   ├── users.html
│   ├── user_detail.html
│   └── currencies.html
├── utils/
│   └── currencies_api.py      # функция get_currencies
├── myapp.py                   # запуск сервера и маршрутизация
├── tests.py                   # тесты
├── README.md                  # этот файл
└── .gitignore
```

Ключевые файлы:
- `myapp.py` - контроллер/HTTPServer, маршрутизация, инициализация Jinja2 и запуск сервера.
- `models/entities.py` - реализации классов предметной области (моделей).
- `utils/currencies_api.py` - функция `get_currencies` для получения актуальных курсов.
- `templates/*.html` - представления на Jinja2.
- `tests.py` - примеры тестов для моделей и логики.

## 4. Описание реализации

**Реализация моделей и их свойств**

Модели реализованы как классы в `models/entities.py`. Для каждого свойства предусмотрены геттеры и сеттеры с проверкой типов и базовой валидацией (например, `value` - float >= 0, `nominal` - положительное целое). Пример шаблона для поля:

```python
class Currency:
    def __init__(self, id: str, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self._id = id
        self.char_code = char_code
        self.num_code = num_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: float) -> None:
        if not isinstance(v, (int, float)):
            raise TypeError("Курс не может быть отрицательным")
        if v < 0:
            raise ValueError("Номинал должен быть больше 0")
        self._value = float(v)
```

Все сеттеры используют явную проверку типов и выбрасывают `TypeError`/`ValueError` при некорректных значениях.

**Маршруты и обработка запросов**

Контроллер реализован в `myapp.py` на базе `http.server.HTTPServer` и `BaseHTTPRequestHandler`. Маршрутизация - через анализ `self.path` и `urllib.parse.parse_qs`.

Поддерживаемые маршруты:
- `/` - главная страница (информация о приложении и авторе)
- `/users` - список пользователей
- `/user?id=...` - данные о конкретном пользователе и его подписках
- `/currencies` - список валют с текущими курсами
- `/author` - информация об авторе

Пример обработки запроса и рендеринга шаблона:

```python
from urllib.parse import urlparse, parse_qs

parsed = urlparse(self.path)
path = parsed.path
qs = parse_qs(parsed.query)

if path == '/users':
    users = user_repo.list_all()
    html = template_users.render(users=users)
    self.wfile.write(html.encode('utf-8'))
```

**Jinja2: инициализация и использование**

Шаблонизатор инициализируется один раз при старте приложения (в `myapp.py`):

```python
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template_index = env.get_template('index.html')
```

Пояснение: `Environment` кэширует шаблоны и хранит настройки Jinja2; инициализация один раз повышает производительность и упрощает тестирование.

**Интеграция `get_currencies`**

Функция `get_currencies()` находится в `utils/currencies_api.py`. Она выполняет HTTP-запрос к внешнему API, парсит XML/JSON и возвращает список объектов или словарей, соответствующих модели `Currency`.

При заходе на `/currencies` контроллер вызывает `get_currencies()`, преобразует результаты в объекты `Currency` и передаёт их в шаблон `currencies.html`. Обновление курсов может вызываться и через кнопку на странице, которая формирует GET-запрос с параметром `?refresh=1`.

## 5. Примеры работы приложения

Ниже указать реальные скриншоты и примеры вывода. Пока - шаблоны мест для вставки.

- Главная страница `/` - файл: `templates/index.html`.
- Список пользователей `/users` - `templates/users.html`.
- Валюты `/currencies` - `templates/currencies.html`.
- Детали пользователя `/user?id=...` - `templates/user_detail.html`.

index
[![image.png](https://i.postimg.cc/DzSTnTGn/image.png)](https://postimg.cc/TyvSJBQ4)
users
[![image.png](https://i.postimg.cc/66LDs3PZ/image.png)](https://postimg.cc/vDTPfQb8)
user_detail
![[Pasted image 20251216203603.png]]

currencies
[![image.png](https://i.postimg.cc/9MB1k4Qn/image.png)](https://postimg.cc/bDsQDwbx)
## 6. Тестирование

В `tests.py` описаны примеры тестов (модуль `unittest` или `pytest`):

- Тесты моделей:
  - проверка корректной установки и чтения свойств
  - проверка выброса исключений при неверных типах/значениях

- Тесты `get_currencies`:
  - мокирование HTTP-ответа (например, через `unittest.mock.patch` или `responses`) и проверка корректного парсинга
  - проверка обработки ошибок сети и неверного формата

- Тесты контроллера:
  - запуск обработчика в тестовом окружении и проверка ответов для `/, /users, /currencies`
  - проверка обработки параметра `id` для `/user`

Пример теста для `Currency.value`:

```python
def test_currency_value_setter_raises():
    c = Currency('R000', '000', 'TST', 'Test', 1.0, 1)
    with pytest.raises(TypeError):
        c.value = 'not-a-number'
    with pytest.raises(ValueError):
        c.value = -5
```

Как запускать тесты:

```bash
python -m pytest tests.py
```

```python
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

## 7. Выводы

- Проблемы при реализации: ручное парсинг XML, обработка ошибок сети и форматирования числа (запятая/точка), аккуратная валидация полей моделей.
- Применение MVC: модель/представление/контроллер чётко разделены - модели в `models`, шаблоны в `templates`, логика маршрутизации в `myapp.py`.
- Новые знания: опыт использования `HTTPServer` и `BaseHTTPRequestHandler`, настройка и кеширование шаблонов Jinja2 через `Environment`, работа с внешними API курсов валют и преобразование ответов в модели.

## Информация о студенте
Иванов ФВ, 2 курс, ИВТ-1.2