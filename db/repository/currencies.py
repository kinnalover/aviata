
from db.models.currencies import Currencies
from db.models.searches import Search
from schemas.searches import SearchCreate, SearchUpdate
from schemas.searches import SearchCreate
from sqlalchemy.orm import Session
from sqlalchemy.types import JSON
from datetime import datetime


def add_daily_currency(currency, db: Session):
    existing_search = db.query(Currencies).filter(Currencies.date == datetime.now().date()).first()
    if existing_search:
        return 0
    currency_object=Currencies(date=datetime.now().date(), currencies=currency)
    db.add(currency_object)
    db.commit()
    db.refresh(currency_object)
    return currency_object

def get_todays_currencies(db: Session):
    existing_search = db.query(Currencies).filter(Currencies.date == datetime.now().date()).first()
    if not existing_search:
        print("Couldn't find today's currency info")
        return 0
    return existing_search.currencies



