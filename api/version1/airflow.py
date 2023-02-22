from datetime import datetime
from api.utils import get_currencies_from_nb_kz, get_items_converted
from core.config import settings
from db.repository.searches import create_new_search, get_seach_by_id, update_search
from schemas.searches import SearchCreate, SearchUpdate
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import asyncio
import json
from uuid import uuid4
import aiohttp
from db.models.searches import Search
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends

router=APIRouter()
async def get_search_results(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            if response.status==200:
                return await response.json()
                
            else:
                raise HTTPException(status_code=response.status)



@router.post("/search")
async def search_airflow(db: Session = Depends(get_db)):
    """Cервис airflow, c методом поиска POST /search который
    отправляет запросы на поиск в сервисы provider-a и provider-b и в ответе
    возвращает уникальный search_id поиска
    {
    "search_id": "d9e0cf5a-6bb8-4dae-8411-6caddcfd52da"
    }
    Однако нужно сразу же записать в бд строку с состониянием PENDING,
     а когда закончится, то поменять статус на  COMPLETED
    """
    search_id=str(uuid4())
    #generating unique id

    search=SearchCreate(search_id=search_id)
    create_new_search(search=search,db=db)
    results=await asyncio.gather(get_search_results(f"http://localhost:{settings.PORT}/provider-a/search"),get_search_results(f"http://localhost:{settings.PORT}/provider-b/search"))
    all_items=results[0]+results[1]



    #Обновляем данные в бд на Сompleted и вставлям данные перелетов
    search_update=SearchUpdate(search_id=search_id, status="COMPLETED",items=all_items)
    update_search(search=search_update, db=db)
    return JSONResponse(content={"search_id":search_id})


@router.get("/results/{search_id}/{currency}")
async def search_results(search_id: str, currency:str,db: Session = Depends(get_db)):
    """:arg search_id -> указываем из метода POST /airflow/search.
    Возвращает ошибку если не найден search_id
    :arg currency -> указываем валюту которую хотим, но только аббреавитуры как USD AUD CNY KZT
    Если валюта не найдена, то возвращает ошибку.
    """
    search_info=get_seach_by_id(search_id,db)
    response={
            "search_id":search_id,
            "status": "PENDING",
            "items": []
        }

    if not search_info:
        raise HTTPException(404,detail="search ID not found")

    if search_info.status=="COMPLETED":
        newlist = sorted(search_info.items, key=lambda d: float(d['pricing']['total']) )
        converted_list=get_items_converted(currency=currency,db=db, process_info=newlist )
        if converted_list[0].get("status"):
            raise HTTPException(404, detail="currency is not valid")
        response.update({"items":converted_list,"status":"COMPLETED"})

    return JSONResponse(content=response)

