import os
from dotenv import load_dotenv
import google.generativeai as genai

class GeminiApiHandler:

    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.environ.get('GEN_AI_API_KEY'))

        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        )

        self.chat_session = self.model.start_chat(
        history=[
        ]
        )

    def get_job_details(self, html_code: str):
        prompt = (
            "you are given an html code of a job post page. you need to find the job requirements and description from"
            f"the page and the time when was the job post created. HTML: {html_code}"
            "Use this JSON schema:"
            "List = {'requirement' : str, 'salary': optional[str], 'relocation_support': bool, 'skills': list[str]}"
            "Return: List"
            "DONOT RETURN ANY RESPONSE OTHER THAN ONLY THE JSON SCHEMA I HAVE PROVIDED. ONLY FILL THEM FROM HTML CODE WHICH WAS PROVIDED"
        )
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        return response
    
    def get_individual_job_links(self, html_code: str):
        prompt = (
            f"you are given an html code of a web page. you need to find the job links. nothing else. Provide the full link of each job."
            "Append base url intelligently if you think that the links as relative to some path. DECIDE INTELLIGENTLY. NORMALLY IT BECOMSE BASE-URL: THEN SOME TAGS RELATED TO JOBS AND THEN JOB ID OR SOMETHING"
            f"HTML: {html_code}\n"
            "Use this JSON schema:\n\n"
            "List = {'links': list[str]}\n"
            "Return: List\n"
            "DONOT RETURN ANY RESPONSE OTHER THAN ONLY THE JSON SCHEMA I HAVE PROVIDED"
        )
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[str]
            ),
        )
        return response
    
    def get_job_relevancy_with_resume(self, resume: str, job: object):
        prompt = (
            f"you are given a resume and a job requirement in object form."
            "Find relevancy of the job with provided resume and return relevancy score within 0-10 and write a mail for this job post mentioning why and how the resume holder fits for the role"
            f"JOB Object: {job}"
            f"Resume: {resume}"
            "Use this JSON schema:"
            "List = {'score': float, 'mail': str, 'job_link': str}"
            "Return: List\n"
            "DONOT RETURN ANY RESPONSE OTHER THAN ONLY THE JSON SCHEMA I HAVE PROVIDED"
        )
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        return response