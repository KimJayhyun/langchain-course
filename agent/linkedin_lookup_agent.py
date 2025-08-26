import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url_tavily

load_dotenv()

API_KEY = os.environ.get("CLOVA_STUDIO_API_KEY")


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        api_key=API_KEY,  # CLOVA Studio API 키
        base_url="https://clovastudio.stream.ntruss.com/v1/openai",  # CLOVA Studio 오픈AI 호환 API URL
        # model="HCX-005",
        model="HCX-007",
        streaming=True,
        extra_body={
            "reasoning": {"effort": "none"},
        },
    )
    # prompt_template = """
    # given the full name {name_of_person}, I want you to get it me a link to their LinkedIn profile page.
    # Your answer should contain only the URL.
    # """

    # prompt = PromptTemplate(
    #     template=prompt_template, input_variables=["name_of_person"]
    # )

    # tools = [
    #     Tool(
    #         name="Crawl Google 4 LinkedIn profile page",
    #         func=get_profile_url_tavily,
    #         description="useful for when you need get the LinkedIn Page URL",
    #     )
    # ]

    # react_prompt = hub.pull("hwchase17/react")

    # agent = create_react_agent(
    #     llm=llm,
    #     tools=tools,
    #     prompt=react_prompt,
    # )

    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # return agent_executor.invoke({"input": prompt.format_prompt(name_of_person=name)})

    def execute_search(inputs):
        name = inputs["name_of_person"]
        search_result = get_profile_url_tavily(name)
        return {"name_of_person": name, "search_result": search_result}

    def format_for_llm(inputs):
        return f"""
        Based on the search results below for {inputs['name_of_person']}, 
        extract and return ONLY the LinkedIn profile URL:
        
        {inputs['search_result']}
        
        Return only the URL, nothing else.
        """

    chain = (
        RunnableLambda(execute_search)
        | RunnableLambda(format_for_llm)
        | llm
        | StrOutputParser()
    )

    return chain.invoke({"name_of_person": name})


if __name__ == "__main__":
    print(lookup("Eden Marco"))
