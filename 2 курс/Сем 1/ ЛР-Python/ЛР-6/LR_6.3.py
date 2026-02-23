import requests
import logging
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


def log_errors(func):
    """Декоратор для логирования ошибок с использованием модуля logging.

    Перехватывает исключения при выполнении функции и записывает их
    в лог с уровнями ERROR (для ошибок запроса) и EXCEPTION (для прочих ошибок).

    Args:
        func (callable): Декорируемая функция.

    Returns:
        callable: Обёрнутая функция с логированием ошибок.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса к API: {e}")
            return None
        except Exception as e:
            logger.exception("Неизвестная ошибка")
            return None
    return wrapper


@log_errors
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """Получает курсы валют с API ЦБ РФ с логированием через logging.

    Возвращает курсы запрошенных валют. Отсутствующие валюты логируются
    как предупреждение (WARNING). Критические ошибки (сетевые, структура ответа)
    логируются как ошибки (ERROR).

    Args:
        currency_codes (list of str): Список ISO-кодов валют (например, ["USD", "JPY"]).
        url (str, optional): URL API (по умолчанию — ЦБ РФ).

    Returns:
        dict or None: Словарь с курсами или None при критической ошибке.

    Example:
        >>> rates = get_currencies(["USD", "CNY"])
        >>> print(rates.get("USD"))
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if "Valute" not in data:
        logger.error("Ответ API не содержит поля 'Valute'")
        return None

    valutes = data["Valute"]
    result = {}
    missing = []

    for code in currency_codes:
        if code in valutes:
            result[code] = valutes[code]["Value"]
        else:
            missing.append(code)

    if missing:
        logger.warning(f"Валюты не найдены в ответе API: {', '.join(missing)}")

    return result

if __name__ == "__main__":
    print(get_currencies(["USD", "EUR", "XYZ"]))  # XYZ — несуществующая валюта
