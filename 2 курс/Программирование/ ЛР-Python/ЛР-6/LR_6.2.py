import requests
import sys
from functools import wraps

def log_errors(func):
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
    print(get_currencies(["USD", "EUR", "XYZ"]))