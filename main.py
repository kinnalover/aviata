from api.base import api_router
from api.utils import get_currencies_from_nb_kz
from core.config import settings
from db.base import Base
from db.session import engine
from db.utils import check_db_connected
from db.utils import check_db_disconnected
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from datetime import datetime


def include_router(app):
    app.include_router(api_router)
    


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    fdate=datetime.now().date().strftime('%d.%m.%Y')
    get_currencies_from_nb_kz(fdate=fdate)
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()
    

@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()