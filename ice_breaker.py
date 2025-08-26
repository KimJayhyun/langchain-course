import os

from dotenv import load_dotenv

# from langchain.chains import LLMChain # deprecated
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agent.linkedin_lookup_agent import lookup
from output_parser import Summary, summary_parser
from third_parties.linkedin import scrape_linkedin_profile

load_dotenv()

API_KEY = os.environ.get("CLOVA_STUDIO_API_KEY")


def ice_break_with(name: str) -> str:
    linkedin_username = lookup(name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    llm = ChatOpenAI(
        api_key=API_KEY,  # CLOVA Studio API 키
        base_url="https://clovastudio.stream.ntruss.com/v1/openai",  # CLOVA Studio 오픈AI 호환 API URL
        # model="HCX-005",
        model="HCX-007",
        streaming=True,
        # extra_body={
        #     "reasoning": {"effort": "none"},
        # },
    )

    summary_prompt = """
        given the LinkedIn information {linkedin_data} about a person I want you to create:
        
        1. A short summary
        2. two interesting facts about them
        """

    prompt = PromptTemplate(
        template=summary_prompt,
        input_variables=["linkedin_data"],
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    chain = prompt | llm | summary_parser

    res = chain.invoke(input={"linkedin_data": linkedin_data})

    return res


if __name__ == "__main__":
    print(ice_break_with("Eden Marco"))
