"""
Основной модуль приложения. Реализует HTTP-сервер и маршрутизацию (Controller).
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import List
from jinja2 import Environment, PackageLoader, select_autoescape

# Импорты моделей и утилит
from models.entities import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies

# Инициализация данных 

# Автор
main_author = Author(name="Иванов Федор", group="ИВТ-1.2")
main_app = App(name="CurrenciesApp", version="1.0", author=main_author)

# Список пользователей
users_db: List[User] = [
    User(1, "Алексей"),
    User(2, "Мария"),
    User(3, "Дмитрий")
]

# Хранилище валют (ключ - ID валюты)
currencies_db: List[Currency] = []

# Подписки 
user_currencies_db: List[UserCurrency] = []

# Настройка Jinja2 
env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Класс обработчика HTTP-запросов. Выполняет роль Front Controller.
    """

    def _render_template(self, template_name: str, context: dict) -> None:
        """
        Рендерит шаблон и отправляет ответ клиенту.

        Args:
            template_name (str): Имя файла шаблона.
            context (dict): Данные для шаблона.
        """
        template = env.get_template(template_name)
        html_content = template.render(**context)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(html_content, "utf-8"))

    def _update_currencies_if_empty(self) -> None:
        """Загружает валюты, если база пуста."""
        if not currencies_db:
            raw_data = get_currencies()
            for item in raw_data:
                currency = Currency(
                    curr_id=item['id'],
                    num_code=item['num_code'],
                    char_code=item['char_code'],
                    name=item['name'],
                    value=item['value'],
                    nominal=item['nominal']
                )
                currencies_db.append(currency)

    def do_GET(self) -> None:
        """Обработка GET запросов (получение данных)."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # 1. Главная страница
        if path == "/":
            self._render_template("index.html", {
                "myapp": main_app.name,
                "version": main_app.version,
                "author_name": main_app.author.name,
                "group": main_app.author.group,
                "navigation": [
                    {'caption': 'Список пользователей', 'href': '/users'},
                    {'caption': 'Курсы валют', 'href': '/currencies'}
                ]
            })

        # 2. Список пользователей
        elif path == "/users":
            self._render_template("users.html", {
                "users": users_db
            })

        # 3. Список валют (обновляется при заходе)
        elif path == "/currencies":
            # Принудительно обновляем или загружаем если пусто
            currencies_db.clear()
            self._update_currencies_if_empty()
            
            self._render_template("currencies.html", {
                "currencies": currencies_db
            })

        # 4. Детали пользователя
        elif path == "/user":
            user_id_list = query_params.get("id")
            if not user_id_list:
                self.send_error(400, "Missing user ID")
                return
            
            user_id = int(user_id_list[0])
            user = next((u for u in users_db if u.id == user_id), None)

            if not user:
                self.send_error(404, "User not found")
                return

            # Обработка добавления подписки 
            new_currency_id = query_params.get("add_currency_id")
            if new_currency_id:
                c_id = new_currency_id[0]
                # Проверка на дубликат
                exists = any(uc.user_id == user.id and uc.currency_id == c_id for uc in user_currencies_db)
                if not exists:
                    # Создаем простой ID для связи
                    new_id = len(user_currencies_db) + 1
                    user_currencies_db.append(UserCurrency(new_id, user.id, c_id))

            # Подготовка данных для отображения
            self._update_currencies_if_empty()
            
            # Находим валюты, на которые подписан пользователь
            user_subs_ids = [uc.currency_id for uc in user_currencies_db if uc.user_id == user.id]
            user_subs_objs = [c for c in currencies_db if c.id in user_subs_ids]

            self._render_template("user_detail.html", {
                "user": user,
                "subscriptions": user_subs_objs,
                "all_currencies": currencies_db
            })
            
        elif path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()

        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self) -> None:
        """Обработка POST запросов (отправка данных)."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/users":
            # 1. Получаем длину тела запроса
            content_length = int(self.headers.get('Content-Length', 0))
            
            # 2. Читаем тело запроса
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # 3. Парсим данные формы
            # parse_qs возвращает словарь типа {'name': ['Значение']}
            data = parse_qs(post_data)
            
            new_name_list = data.get('name')
            if new_name_list:
                new_name = new_name_list[0]
                # Генерируем новый ID (максимальный текущий + 1)
                new_id = max([u.id for u in users_db], default=0) + 1
                
                # Создаем и добавляем пользователя
                new_user = User(new_id, new_name)
                users_db.append(new_user)

            # 4. Редирект обратно на страницу списка 
            self.send_response(303) 
            self.send_header('Location', '/users')
            self.end_headers()
        else:
            self.send_error(501, "Unsupported POST path")


def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    """Запуск сервера."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Сервер остановлен.")


if __name__ == "__main__":
    run()