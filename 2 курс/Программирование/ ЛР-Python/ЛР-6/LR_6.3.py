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