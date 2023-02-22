from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import JSON


class Search(Base):
    search_id = Column(String, primary_key=True, index=True)
    
    status = Column(String, nullable=False)
    items=Column(JSON, nullable=True)
    