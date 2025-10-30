from langgraph.prebuilt import ToolNode
from src.Tools.search_tool import get_search_tool
from src.Tools.hotel_tool import fetch_hotel_rates

class Tools:
    def get_tools():
        """Returns the list of tools used in the chatbot"""

        tools=[get_search_tool,fetch_hotel_rates]

        return tools

    def create_tool_node(tools):
        """
        creates and return a tool node for graph.
        """

        return ToolNode(tools=tools)
