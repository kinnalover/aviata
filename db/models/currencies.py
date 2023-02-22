from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import JSON
from sqlalchemy import Integer

class Currencies(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    currencies=Column(JSON, nullable=False)