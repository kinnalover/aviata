
from db.models.searches import Search
from schemas.searches import SearchCreate, SearchUpdate
from schemas.searches import SearchCreate
from sqlalchemy.orm import Session


def create_new_search(search: SearchCreate, db: Session):
    search_object=Search(**search.dict())
    db.add(search_object)
    db.commit()
    db.refresh(search_object)
    return search_object

def update_search(search: SearchUpdate, db: Session):
    pass
    existing_search = db.query(Search).filter(Search.search_id == search.search_id)
    if not existing_search.first():
        return 0
     
    existing_search.update(search.__dict__)
    db.commit()
    return 1

def get_seach_by_id(search_id: str ,db: Session):
    search_info = db.query(Search).filter(Search.search_id == search_id).first()
    
    return search_info

