import pandas as pd
from pydantic import BaseModel

from perplexity_utils import perplexity_search


def create_prompt(name, location=None, university=None, graduation_year=None, industry=None, employer=None, job_title=None, additional_info=None):
   return f"""
    You are a person finder AI. Your task is to find information about a person based on the provided details. 
    Here are the details you have:

    - Name: {name}
    - Location: {location if location else 'Not specified'} 
    - University: {university if university else 'Not specified'}
    - Graduation Year: {graduation_year if graduation_year else 'Not specified'}
    - Industry: {industry if industry else 'Not specified'}
    - Employer: {employer if employer else 'Not specified'}
    - Job Title: {job_title if job_title else 'Not specified'}
    - Additional Info: {additional_info if additional_info else 'Not specified'}
     
    It is very important that your sources identify the correct person, verifying by checking alignment with the information above
    Air on the side of caution- it is OK to return no results if you are not sure.

    Please return the following information, matching the provided json schema. If you cannot find any of the requested information, return 'Not Found' for that field.
    In cases where the information has already been provided, return the field given in the prompt.

    - Location: where the person urrently resides
    - University: where the person studied, return multiple if applicable with the degree in parentheses
    - Graduation Year: when the person graduated, return multiple if applicable with the degree in parentheses
    - Industry: the industry the person works in
    - Employer: the company the person works for
    - Job Title: the person's current job title
    - LinkedIn Link: the person's LinkedIn profile link
    - Summary of Additional Info: a brief summary (max 3 sentences) of any additional information found

    """

class OutputSchema(BaseModel):
    location: str
    university: str
    graduation_year: str
    industry: str
    employer: str
    job_title: str
    linkedin_link: str
    summary_of_additional_info: str

def get_person_info(name, location=None, university=None, graduation_year=None, industry=None, employer=None, job_title=None, linkedin_link=None, additional_info=None):
    
    prompt = create_prompt(name, location, university, graduation_year, industry, employer, job_title, additional_info)
    output_schema = OutputSchema.model_json_schema()
    
    response = perplexity_search(prompt, output_schema=output_schema)
    content = response['choices'][0]['message']['content']
    search_results = pd.DataFrame(response['search_results'])

    return content, search_results

    

