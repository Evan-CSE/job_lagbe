import urllib.request
from service.llm import GeminiApiHandler
from service.dynamic_html_resolver import DynamicHTMLFetcher
import json

class JobLinkFinder:
    gemini: GeminiApiHandler
    def __init__(self):
        self.gemini = GeminiApiHandler()

    def find_job_links(self):
        all_links = ""
        with open('career_sites.txt', 'r') as career_links:
            all_links = career_links.read()
        all_link_list = all_links.split('\n')
        actual_job_links = self.get_individual_job_links_from_career_page(all_link_list[0])

        for job_link in actual_job_links:
            job_details = self.crawl_individual_job_link(job_link)
            json_str = (job_details._result.candidates[0].content.parts[0].text)
            data = json.loads(json_str)
            data['link'] = job_link
            # print(data)
            with open('job_description.txt', 'a', encoding='utf-8') as file:
                file.write(json_str + '\n\n\n\n\n\n')
            application_details = self.find_relevancy_with_resume(data)
            with open('recommended_job', 'a', encoding='utf-8') as file:
                 file.write(application_details)
            

    def find_relevancy_with_resume(self, job_details: object):
         #read resume
         resume = ''
         with open('resume.txt', 'r') as fl:
              resume = fl.read()
         details = self.gemini.get_job_relevancy_with_resume(resume=resume, job=job_details)
         json_str = (details._result.candidates[0].content.parts[0].text)
         data = json.loads(json_str)
         return json_str
        


    def get_individual_job_links_from_career_page(self, link: str):
        fetcher = DynamicHTMLFetcher()
        html_content = fetcher.get_dynamic_html(link, wait_time=5)

        if html_content:
            print("Successfully fetched HTML")
            try:
                with open('html.txt', 'w', encoding='utf-8') as file:
                    file.write(html_content)
                print(f"Successfully wrote content to html.txt")
            except Exception as e:
                print(f"Error writing to file: {str(e)}")
            ans = self.gemini.get_individual_job_links(html_content)
            json_str = (ans._result.candidates[0].content.parts[0].text)
            data = json.loads(json_str)
            print(data)
            with open('individual_links.txt', 'a', encoding='utf-8') as file:
                    file.write(json_str)
            # print(ans.response.result.candidates[0].content.parts[0].text)
            return data
        else:
            print("Failed to fetch HTML")


    def crawl_individual_job_link(self, link: str):
        fetcher = DynamicHTMLFetcher()
        html_content = fetcher.get_dynamic_html(link, wait_time=5)
        with open('job_description.txt', 'a', encoding='utf-8') as file:
                    file.write(html_content + '\n\n\n\n\n\n\n')
        return self.get_job_details(html_content)


    def get_job_details(self, html: str):
        ans = self.gemini.get_job_details(html)
        return ans
    