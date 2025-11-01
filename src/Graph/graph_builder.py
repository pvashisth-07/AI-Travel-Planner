from langgraph.graph import StateGraph, START, END
from src.Tools.tool_assembly import Tools
from src.State.state import State
from src.nodes.query_generator import QueryGenerator
from src.nodes.grade_query import GradeQuery
from src.nodes.itinerary_node import ItenaryNode
from src.nodes.validate_itinerary_node import Validate_Itinerary_Node


class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def ai_traveller_planner_graph(self):
        """
        Builds AI Traveller Planner DAG:
        START → QueryGenerator → GradeQuery → (PASS → Itinerary) / (FAIL → QueryGenerator)
            Itinerary → ValidateItinerary → (PASS → END) / (FAIL → Itinerary)
        """

        #Define Tools
        tools = Tools.get_tools()
        tool_node = Tools.create_tool_node(tools)

        #Define Nodes
        query_generator = QueryGenerator()
        grade_query = GradeQuery()
        itinerary_node = ItenaryNode()
        validate_itinerary = Validate_Itinerary_Node()

        #Add Nodes to Graph
        self.graph_builder.add_node("QueryGenerator", query_generator.process)
        self.graph_builder.add_node("GradeQuery", grade_query.process)
        self.graph_builder.add_node("ItenaryGenerator", itinerary_node.process)
        self.graph_builder.add_node("ValidateItenary", validate_itinerary.process)
        self.graph_builder.add_node("ToolNode", tool_node)

        #Edges
        self.graph_builder.add_edge(START, "QueryGenerator")
        self.graph_builder.add_edge("QueryGenerator", "GradeQuery")

        # Grade Query: if FAIL → back to QueryGenerator, else → Itinerary Generator
        self.graph_builder.add_conditional_edges(
            "GradeQuery",
            lambda state: state["graded_query"],
            {
                "PASS": "ItenaryGenerator",
                "FAIL": "QueryGenerator"
            }
        )

        # Itinerary generator uses external tools
        self.graph_builder.add_edge("ToolNode", "ItenaryGenerator")

        # After itinerary generation, validate it
        self.graph_builder.add_edge("ItenaryGenerator", "ValidateItenary")

        # If validation fails → regenerate itinerary, else → END
        self.graph_builder.add_conditional_edges(
            "ValidateItenary",
            lambda state: state["validation_result"],
            {
                "PASS": END,
                "FAIL": "ItenaryGenerator"
            }
        )

        #Compile Graph
        return self.graph_builder.compile()
