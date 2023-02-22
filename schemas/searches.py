
from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel




class SearchBase(BaseModel):
    search_id: Optional[str]=None
    status: Optional[str] = "PENDING"
    items: Optional[list] = []
    


class SearchCreate(SearchBase):
    search_id: str
    
class SearchUpdate(SearchBase):
    search_id: str
    status: str
    items: list
    


