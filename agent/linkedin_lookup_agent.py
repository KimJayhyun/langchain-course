import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
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
    prompt_template = """
    given the full name {name_of_person}, I want you to get it me a link to their LinkedIn profile page.
    Your answer should contain only the URL.
    """

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["name_of_person"]
    )

    tools = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=react_prompt,
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor.invoke({"input": prompt.format(name_of_person=name)})


if __name__ == "__main__":
    print(lookup("Eden Marco"))
