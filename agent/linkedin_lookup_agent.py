import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    prompt_template = """
    given the full name {name_of_person}, I want you to get it me a link to their LinkedIn profile page.
    Your answer should contain only the URL.
    """

    prompt = PromptTemplate.from_template(
        template=prompt_template, input_variables=["name_of_person"]
    )

    tools = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            funct="",
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

    # return agent.invoke({"input": prompt.format(name_of_person=name)})
