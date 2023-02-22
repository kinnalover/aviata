
from fastapi import APIRouter

router = APIRouter()

from fastapi.responses import HTMLResponse





# Define a route to serve the index.html file
@router.get("/", response_class=HTMLResponse)
async def read_main():
    with open("static/index.html", encoding="UTF-8") as file:
        return file.read()