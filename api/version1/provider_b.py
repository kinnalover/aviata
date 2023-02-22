from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
import json
from core.config import settings



router=APIRouter()
@router.post("/search")
async def search_provider_b():
    print("search B starts sleeping 60 sec")
    await asyncio.sleep(settings.TIMEOUT_B)
    with open("tests/response_a.json") as f:
        return JSONResponse(content=json.load(f))
