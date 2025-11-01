from langgraph.prebuilt import ToolNode
from src.Tools.search_tool import get_search_tool
from src.Tools.hotel_tool import fetch_hotel_rates

class Tools:
    """Handles assembling all available tools for the travel planner."""

    @staticmethod
    def get_tools():
        """Returns the list of callable tools used in the chatbot"""
        return [get_search_tool, fetch_hotel_rates]

    @staticmethod
    def create_tool_node(tools):
        """Creates and returns a ToolNode for the LangGraph."""
        return ToolNode(tools=tools)
