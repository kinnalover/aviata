from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
import json




router=APIRouter()
@router.post("/search")
async def search_provider_b():
    print("search B starts sleeping 60 sec")
    await asyncio.sleep(60)
    with open("tests/response_a.json") as f:
        return JSONResponse(content=json.load(f))
