from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter profiles"""
    search = TavilySearchResults()

    return search.run(name)
