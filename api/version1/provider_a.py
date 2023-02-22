from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
from core.config import settings
import json


router=APIRouter()
@router.post("/search")
async def search_provider_a():
    """
    Ждет 30 секунд. И возвращает содержимое из файла response_a.json.
    """
    print("search A starts sleeping 30 sec")
    await asyncio.sleep(settings.TIMEOUT_A)
    with open("resourses/response_a.json") as f:
        return JSONResponse(content=json.load(f))
