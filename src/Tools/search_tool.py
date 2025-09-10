
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

@tool
def get_search_tool():
    """Returns the search tool for websearch."""
    tool = TavilySearch(
    max_results=5,
    topic="general",
    )
    return tool