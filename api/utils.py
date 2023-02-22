
import json
from typing import Dict, Any, List

from db.repository.currencies import add_daily_currency, get_todays_currencies
import feedparser
from db.session import SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
def get_currencies_from_nb_kz(fdate:str)->dict:
    
    
    # Собираем URL для RSS-ленты
    url = f"https://www.nationalbank.kz/rss/get_rates.cfm?fdate={fdate}"
    
    try:
        # Парсим RSS-ленту и получаем список элементов <item>
        feed = feedparser.parse(url)
        items = feed.entries
        
        # Создаем словарь для хранения данных
        data = {}
        
        # Парсим каждый элемент <item>
        for item in items:
            # Получаем заголовок и описание элемента
            title = item.title
            description = item.description
            
            # Добавляем данные в словарь
            item_data = {
                title: description
            }
            data.update(item_data)
        
        # Сохраняем данные в формате JSON в файл
        
        data_json=json.dumps(data)
        db = SessionLocal()
        
        res=add_daily_currency(currency=data_json, db=db)
        if not res:
            print("Currencies downloaded already")
        
        return data

    except Exception as e:
        # Обрабатываем ошибку, если RSS-лента не доступна или URL некорректен
        print(f"Ошибка: {e}")


def get_items_converted(currency: str, db: Session, process_info: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Fetch today's currency rates from the database
    currency_json = get_todays_currencies(db)
    # Convert currency rates to dictionary
    currency_values: Dict[str, float] = json.loads(currency_json)

    # Check if the provided currency exists in the currency rates dictionary
    if currency.lower() != "kzt":
        get_needed_currency = currency_values.get(currency)
        if not get_needed_currency:
            return {"status": "Error: the currency you provided doesn't exist"}

    for flight in process_info:
        
        currency_of_flight = flight.get("pricing").get("currency")
        total_price_of_flight = flight.get("pricing").get("total")

        # Check if the currency of the flight exists in our currency rates dictionary
        price_of_currency=currency_values.get(currency_of_flight)
        if not price_of_currency:
            # If the currency is not in our dictionary, pass unconverted values
            flight.update({
                "price": {
                    "amount": total_price_of_flight,
                    "currency": currency_of_flight
                }
            })

        # Convert the currency to the requested currency
        if currency.lower() == "kzt":
            converted_price = float(total_price_of_flight) * float(price_of_currency)
        else:
            converted_price = float(total_price_of_flight) * float(price_of_currency) / float(get_needed_currency)

        # Update the price of the flight with the converted amount and currency
        flight.update({
            "price": {
                "amount": "{:.2f}".format(converted_price),
                "currency": str(currency)
            }
        })

    return process_info
