from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch

def get_search_tool():
    """Returns the search tool for websearch."""
    tool = TavilySearch(
    max_results=5,
    topic="general",
    )
    return tool