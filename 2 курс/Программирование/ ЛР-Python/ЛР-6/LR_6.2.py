import requests
import sys
from functools import wraps

def log_errors(func):
    """Декоратор для перехвата и вывода ошибок в stdout.

    Перехватывает исключения, связанные с запросами к API и общие ошибки,
    выводит их в stdout и возвращает None вместо вызова функции.

    Args:
        func (callable): Декорируемая функция.

    Returns:
        callable: Обёрнутая функция с обработкой ошибок.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к API: {e}", file=sys.stdout)
            return None
        except Exception as e:
            print(f"Неизвестная ошибка: {e}", file=sys.stdout)
            return None
    return wrapper


@log_errors
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """Получает курсы валют с API ЦБ РФ с автоматической обработкой ошибок.

    Аналогично функции из 1-й итерации, но обёрнута в декоратор `@log_errors`,
    который перехватывает исключения и выводит их в stdout.

    Args:
        currency_codes (list of str): Список кодов валют (например, ["USD", "EUR"]).
        url (str, optional): URL API .

    Returns:
        dict or None: Словарь с курсами или None при ошибке.

    Example:
        >>> rates = get_currencies(["USD", "GBP"])
        >>> if rates: print(rates["USD"])
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if "Valute" not in data:  
        return None

    valutes = data["Valute"]
    result = {}
    for code in currency_codes:
        if code in valutes:
            result[code] = valutes[code]["Value"]
        else:
            print(f"Ошибка: валюты {code} нет в ответе", file=sys.stdout)

    return result


# Пример использования
if __name__ == "__main__":
    print(get_currencies(["USD", "EUR", "XYZ"])) # XYZ — несуществующая валюта
