import requests
import sys

def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """Получает курсы указанных валют с официального API ЦБ РФ.

    Функция делает GET-запрос к указанному URL, извлекает курсы валют из ответа
    и возвращает словарь с кодами валют и их значениями в рублях.
    При возникновении ошибок запроса или отсутствии данных — выводит сообщение
    в stdout и возвращает None.

    Args:
        currency_codes (list of str): Список кодов валют (например, ["USD", "EUR"]).
        url (str, optional): URL API для получения курсов. По умолчанию —
            официальный ежедневный JSON от ЦБ РФ.

    Returns:
        dict or None: Словарь вида {"USD": 90.5, "EUR": 98.2} или None в случае ошибки.

    Example:
        >>> rates = get_currencies(["USD", "EUR"])
        >>> print(rates["USD"])  
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}", file=sys.stdout)
        return None

    if "Valute" not in data:
        print("Ошибка: в ответе нет данных о валютах", file=sys.stdout)
        return None

    valutes = data["Valute"]
    result = {}
    for code in currency_codes:
        if code in valutes:
            result[code] = valutes[code]["Value"]
        else:
            print(f"Ошибка: валюты {code} нет в ответе", file=sys.stdout)
    
    return result
