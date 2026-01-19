from fastapi import APIRouter, FastAPI

from routers.health_router import router as health_router
from routers.ml_mgm_router import router as ml_mgm_router

from services.lifespan_model_load import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(ml_mgm_router)
