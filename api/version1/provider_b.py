from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
import json
from core.config import settings



router=APIRouter()
@router.post("/search")
async def search_provider_b():
    """
    Этот метод ничего не принимает.
    Ждет 60 секунд а затем читает из response_b.json и возращает содержимое.
    """
    print("search B starts sleeping 60 sec")
    await asyncio.sleep(settings.TIMEOUT_B)
    with open("resourses/response_b.json") as f:
        return JSONResponse(content=json.load(f))
