from fastapi import APIRouter
from controller.crawling_site_uploader import router as crawler_router

router = APIRouter()

router.include_router(router=crawler_router, prefix="/add_to_list", tags=["Add to Crawler list"])