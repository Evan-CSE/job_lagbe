from fastapi import FastAPI, APIRouter
from api.v1.router import router as main_router


app = FastAPI()
router = APIRouter()


app.include_router(main_router)