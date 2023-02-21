from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import asyncio
import json
from uuid import uuid4
import aiohttp


router=APIRouter()
async def get_search_results(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            if response.status==200:
                return await response.json()
                
            else:
                raise HTTPException(status_code=response.status)



@router.post("/search")
async def search_airflow():
    search_id=str(uuid4())
    results=await asyncio.gather(get_search_results("http://localhost:8000/provider-a/search"),get_search_results("http://localhost:8000/provider-b/search"))
    # await asyncio.create_task(await get_search_results("http://localhost:8000/provider-a/search"))
    # await asyncio.create_task(await get_search_results("http://localhost:8000/provider-b/search"))
    return JSONResponse(content={"search_id":search_id})


@router.get("/results/{search_id}/{currency}")
async def search_results():
    pass