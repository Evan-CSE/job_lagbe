from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from service.job_link_finder import JobLinkFinder

router = APIRouter()

@cbv(router)
class WebsiteCrawlerDumper:

    def __init__(self):
        pass

    @router.post('/')
    async def append_job_url(self, links: list[str]) -> bool:
        try:
            with open('career_sites.txt', 'a') as fl:
                for link in links:
                    fl.write(link + '\n')
            return True
        except Exception as ex:
            raise
        
    @router.get('/')
    async def crawl_job_links(self):
        finder = JobLinkFinder()
        finder.find_job_links()