import os

import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape a LinkedIn profile.
    Manually scrape a information from the LinkedIn profile.
    """

    if mock:
        api_endpoint = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"

        response = requests.get(api_endpoint)
        return response.json()

    api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"

    body = {
        "apikey": os.getenv("SCRAPIN_API_KEY"),
        "url": linkedin_profile_url,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(api_endpoint, json=body, headers=headers)

    return response.json()


if __name__ == "__main__":
    load_dotenv()

    linkedin_profile_url = "https://www.linkedin.com/in/kimjayhyun/"
    information = scrape_linkedin_profile(linkedin_profile_url, mock=True)

    summary_template = """
    ## Given Information
    {information}

    ## Task
    1. make a short summary of the given information
    2. extract two interesting facts from the given information
    """

    summary_prompt_template = PromptTemplate(
        template=summary_template, input_variables=["information"]
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": information})

    print(res.content)

    with open("output.txt", "w") as f:
        f.write(res.content)
