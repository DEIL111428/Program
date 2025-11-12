import requests
import sys

def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
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
