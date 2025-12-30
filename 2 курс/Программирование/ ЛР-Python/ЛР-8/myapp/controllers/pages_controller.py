"""
Модуль контроллера страниц.

Содержит логику для рендеринга HTML-страниц с использованием Jinja2.
Это слой View в архитектуре MVC.

Классы:
    - PagesController: контроллер для рендеринга страниц
"""

from typing import Dict, Any
from jinja2 import Environment


class PagesController:
    """
    Контроллер для рендеринга HTML-страниц.

    Использует Jinja2 для быстрого и безопасного рендеринга шаблонов.

    Атрибуты:
        env (Environment): Окружение Jinja2 для загрузки шаблонов.
    """

    def __init__(self, env: Environment) -> None:
        """
        Инициализирует контроллер страниц.

        Args:
            env (Environment): Окружение Jinja2.
        """
        self.env = env

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Рендерит шаблон с заданным контекстом.

        Args:
            template_name (str): Имя файла шаблона в папке templates/.
            context (Dict[str, Any]): Словарь данных для подстановки в шаблон.

        Returns:
            str: HTML-строка рендеренного шаблона.

        Raises:
            jinja2.TemplateNotFound: Если шаблон не найден.
        """
        template = self.env.get_template(template_name)
        return template.render(**context)

    def render_index(
        self,
        app_name: str,
        version: str,
        author_name: str,
        group: str,
        navigation: list
    ) -> str:
        """
        Рендерит главную страницу приложения.

        Args:
            app_name (str): Название приложения.
            version (str): Версия приложения.
            author_name (str): Имя автора.
            group (str): Группа автора.
            navigation (list): Список навигационных ссылок.

        Returns:
            str: HTML главной страницы.
        """
        context = {
            'myapp': app_name,
            'version': version,
            'author_name': author_name,
            'group': group,
            'navigation': navigation
        }
        return self.render_template('index.html', context)

    def render_users(self, users: list) -> str:
        """
        Рендерит страницу со списком пользователей.

        Args:
            users (list): Список пользователей.

        Returns:
            str: HTML страницы пользователей.
        """
        context = {'users': users}
        return self.render_template('users.html', context)

    def render_user_detail(
        self,
        user: Dict[str, Any],
        subscriptions: list,
        all_currencies: list
    ) -> str:
        """
        Рендерит страницу с информацией о пользователе и его подписками.

        Args:
            user (Dict[str, Any]): Данные пользователя.
            subscriptions (list): Валюты, на которые подписан пользователь.
            all_currencies (list): Все доступные валюты.

        Returns:
            str: HTML страницы с информацией о пользователе.
        """
        context = {
            'user': user,
            'subscriptions': subscriptions,
            'all_currencies': all_currencies
        }
        return self.render_template('user_detail.html', context)

    def render_currencies(self, currencies: list) -> str:
        """
        Рендерит страницу со списком валют.

        Args:
            currencies (list): Список валют.

        Returns:
            str: HTML страницы валют.
        """
        context = {'currencies': currencies}
        return self.render_template('currencies.html', context)
