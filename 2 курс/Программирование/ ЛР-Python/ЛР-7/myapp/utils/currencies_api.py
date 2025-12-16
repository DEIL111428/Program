"""
Модуль для взаимодействия с внешним API ЦБ РФ.
"""

import logging
import requests
from typing import List, Dict, Any

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_currencies(url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> List[Dict[str, Any]]:
    """
    Получает список валют с API ЦБ РФ.

    Args:
        url (str): URL для запроса JSON.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о валютах.
        Возвращает пустой список в случае ошибки.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "Valute" not in data:
            logger.error("Ответ API не содержит ключа 'Valute'")
            return []

        # Преобразуем словарь Valute в список для удобства создания моделей
        currencies_data = []
        for key, val in data["Valute"].items():
            currencies_data.append({
                "id": val.get("ID"),
                "num_code": val.get("NumCode"),
                "char_code": val.get("CharCode"),
                "name": val.get("Name"),
                "value": val.get("Value"),
                "nominal": val.get("Nominal")
            })
        
        logger.info(f"Загружено {len(currencies_data)} валют.")
        return currencies_data

    except requests.RequestException as e:
        logger.error(f"Ошибка сети при получении валют: {e}")
        return []
    except ValueError as e:
        logger.error(f"Ошибка парсинга JSON: {e}")
        return []