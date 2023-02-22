from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
from core.config import settings
import json


router=APIRouter()
@router.post("/search")
async def search_provider_a():
    print("search A starts sleeping 30 sec")
    await asyncio.sleep(settings.TIMEOUT_A)
    with open("tests/response_a.json") as f:
        return JSONResponse(content=json.load(f))
