"""
Основной модуль приложения.

Реализует HTTP-сервер и маршрутизацию (Router/Controller).
Использует MVC архитектуру с разделением контроллеров на модули.

Основные компоненты:
    - DatabaseController: управление БД и CRUD операциями
    - CurrenciesController: бизнес-логика валют
    - UsersController: бизнес-логика пользователей
    - PagesController: рендеринг страниц
    - MyHTTPRequestHandler: обработчик HTTP запросов

Маршруты:
    GET /              - главная страница
    GET /users         - список пользователей
    GET /user?id=...   - информация о пользователе
    GET /currencies    - список валют
    GET /currency/delete?id=... - удаление валюты
    GET /currency/update?id=...&value=... - обновление курса
    POST /users        - создание пользователя
    POST /subscribe    - подписка на валюту
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Optional
from jinja2 import Environment, PackageLoader, select_autoescape

# Импорты контроллеров
from controllers.database_controller import (
    DatabaseController,
    UserCRUD,
    CurrencyCRUD,
    UserCurrencyCRUD
)
from controllers.currencies_controller import CurrenciesController
from controllers.users_controller import UsersController
from controllers.pages_controller import PagesController

# Импорты моделей и утилит
from models.entities import Author, App
from utils.currencies_api import get_currencies

# Инициализация Jinja2 
env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape(['html', 'xml'])
)

# Инициализация БД и контроллеров
db_controller = DatabaseController()
user_crud = UserCRUD(db_controller)
currency_crud = CurrencyCRUD(db_controller)
user_currency_crud = UserCurrencyCRUD(db_controller)

# Бизнес-логика контроллеры
currencies_controller = CurrenciesController(currency_crud)
users_controller = UsersController(user_crud, user_currency_crud)

# Контроллер для рендеринга страниц
pages_controller = PagesController(env)

# Инициализация данных приложения
main_author = Author(name="Иванов Федор", group="ИВТ-1.2")
main_app = App(name="CurrenciesApp", version="2.0", author=main_author)

# Создание стартовых пользователей
_startup_users = [
    ("Алексей",),
    ("Мария",),
    ("Дмитрий",)
]

for user_name in _startup_users:
    users_controller.create_user(user_name[0])


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Обработчик HTTP-запросов.

    Реализует маршрутизацию запросов к соответствующим контроллерам.
    Обеспечивает обработку GET и POST запросов, валидацию и рендеринг ответов.

    Методы:
        do_GET: обработка GET запросов
        do_POST: обработка POST запросов
        log_message: переопределяется для отключения логирования (по желанию)
    """

    def do_GET(self) -> None:
        """
        Обработка GET запросов.

        Маршруты:
            /              - главная страница
            /users         - список пользователей
            /user?id=...   - информация о пользователе
            /currencies    - список валют
            /currency/delete?id=... - удаление валюты
            /currency/update?id=...&value=... - обновление курса
            /favicon.ico   - иконка браузера
        """
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        try:
            # 1. Главная страница
            if path == "/":
                html_content = pages_controller.render_index(
                    app_name=main_app.name,
                    version=main_app.version,
                    author_name=main_app.author.name,
                    group=main_app.author.group,
                    navigation=[
                        {'caption': 'Список пользователей', 'href': '/users'},
                        {'caption': 'Курсы валют', 'href': '/currencies'}
                    ]
                )
                self._send_response(html_content)

            # 2. Список пользователей
            elif path == "/users":
                users = users_controller.get_all_users()
                html_content = pages_controller.render_users(users)
                self._send_response(html_content)

            # 3. Информация о пользователе и подписки
            elif path == "/user":
                user_id_list = query_params.get("id")
                if not user_id_list:
                    self.send_error(400, "Missing user ID")
                    return

                try:
                    user_id = int(user_id_list[0])
                except ValueError:
                    self.send_error(400, "Invalid user ID")
                    return

                user = users_controller.get_user(user_id)
                if not user:
                    self.send_error(404, "User not found")
                    return

                # Обработка подписки на валюту
                add_currency_id = query_params.get("add_currency_id")
                if add_currency_id:
                    currency_id = add_currency_id[0]
                    users_controller.subscribe_to_currency(user_id, currency_id)

                # Получаем подписки пользователя
                subscriptions = users_controller.get_user_subscriptions(user_id)
                all_currencies = currencies_controller.get_all_currencies()

                html_content = pages_controller.render_user_detail(
                    user=user,
                    subscriptions=subscriptions,
                    all_currencies=all_currencies
                )
                self._send_response(html_content)

            # 4. Список валют
            elif path == "/currencies":
                # Загружаем валюты из API если БД пуста
                all_currencies = currencies_controller.get_all_currencies()
                if not all_currencies:
                    api_data = get_currencies()
                    currencies_controller.load_currencies_from_api(api_data)
                    all_currencies = currencies_controller.get_all_currencies()

                html_content = pages_controller.render_currencies(all_currencies)
                self._send_response(html_content)

            # 5. Удаление валюты
            elif path == "/currency/delete":
                currency_id = query_params.get("id")
                if currency_id:
                    currencies_controller.delete_currency(currency_id[0])
                self._redirect("/currencies")

            # 6. Обновление курса валюты
            elif path == "/currency/update":
                currency_id = query_params.get("id")
                new_value = query_params.get("value")
                if currency_id and new_value:
                    try:
                        value = float(new_value[0])
                        currencies_controller.update_currency_value(currency_id[0], value)
                    except (ValueError, IndexError):
                        pass
                self._redirect("/currencies")

            # 7. Удаление пользователя
            elif path == "/user/delete":
                user_id = query_params.get("id")
                if user_id:
                    try:
                        users_controller.delete_user(int(user_id[0]))
                    except ValueError:
                        pass
                self._redirect("/users")

            # 8. Браузерная иконка
            elif path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()

            else:
                self.send_error(404, "Page Not Found")

        except Exception as e:
            print(f"Ошибка при обработке GET: {e}")
            self.send_error(500, "Internal Server Error")

    def do_POST(self) -> None:
        """
        Обработка POST запросов.

        Маршруты:
            POST /users        - создание нового пользователя
            POST /subscribe    - подписка на валюту
        """
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)

            # 1. Создание пользователя
            if path == "/users":
                name_list = data.get('name')
                if name_list:
                    try:
                        users_controller.create_user(name_list[0])
                    except ValueError:
                        pass
                self._redirect("/users")

            # 2. Подписка на валюту
            elif path == "/subscribe":
                user_id = data.get('user_id')
                currency_id = data.get('currency_id')
                if user_id and currency_id:
                    try:
                        users_controller.subscribe_to_currency(
                            int(user_id[0]),
                            currency_id[0]
                        )
                    except ValueError:
                        pass
                    self._redirect(f"/user?id={user_id[0]}")
                else:
                    self.send_error(400, "Missing parameters")

            else:
                self.send_error(501, "Unsupported POST path")

        except Exception as e:
            print(f"Ошибка при обработке POST: {e}")
            self.send_error(500, "Internal Server Error")

    def _send_response(self, html_content: str) -> None:
        """
        Отправляет HTML ответ клиенту.

        Args:
            html_content (str): HTML контент для отправки.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(html_content, "utf-8"))

    def _redirect(self, location: str) -> None:
        """
        Отправляет редирект на новый URL.

        Args:
            location (str): URL для редиректа.
        """
        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()

    def log_message(self, format_str: str, *args) -> None:
        """Переопределяется для подавления стандартного логирования."""
        pass




def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port: int = 8000) -> None:
    """
    Запускает HTTP сервер приложения.

    Args:
        server_class: Класс сервера (по умолчанию HTTPServer).
        handler_class: Класс обработчика запросов.
        port (int): Порт для запуска сервера (по умолчанию 8000).
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}...")
    print(f"Перейдите на http://localhost:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        httpd.server_close()
        db_controller.close()
        print("Сервер остановлен.")


if __name__ == "__main__":
    run()