from api.version1 import airflow
from api.version1 import provider_b
from api.version1 import provider_a
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(provider_a.router, prefix="/provider-a", tags=["provider-a"])
api_router.include_router(provider_b.router, prefix="/provider-b",tags=["provider-b"])
api_router.include_router(airflow.router, prefix="/airflow",tags=["airflow"])
