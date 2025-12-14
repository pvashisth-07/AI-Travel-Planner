from langgraph.graph import StateGraph, START, END
from src.Tools.tool_assembly import Tools
from src.State.state import State
from src.nodes.query_generator import QueryGenerator
from src.nodes.grade_query import GradeQuery
from src.nodes.itinerary_node import ItineraryNode
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
        query_generator = QueryGenerator(self.llm)
        grade_query = GradeQuery(self.llm)
        itinerary_node = ItineraryNode(self.llm)
        validate_itinerary = Validate_Itinerary_Node(self.llm)

        #Add Nodes to Graph
        self.graph_builder.add_node("QueryGenerator", query_generator.process)
        self.graph_builder.add_node("GradeQuery", grade_query.process)
        self.graph_builder.add_node("ItenaryGenerator", itinerary_node.process)
        self.graph_builder.add_node("ValidateItenary", validate_itinerary.process)
        
        #self.graph_builder.add_node("ToolNode", tool_node)

        #Edges
        self.graph_builder.add_conditional_edges(
            START,
            lambda state: "SKIP" if "structured_query" in state else "RUN",
            {
                "SKIP": "GradeQuery",
                "RUN": "QueryGenerator"
            }
        )

        self.graph_builder.add_edge("QueryGenerator", "GradeQuery")

        # Conditional edge: grading result
        self.graph_builder.add_conditional_edges(
            "GradeQuery",
            lambda state: state.get("graded_query", ""),
            {
                "PASS": "ItenaryGenerator",         # connect to tool usage next
                "FAIL": "QueryGenerator"    # retry query generation
            }
        )

        # Flow 2: ToolNode → Itinerary generation → Validation
        #self.graph_builder.add_edge("ToolNode", "ItenaryGenerator")
        self.graph_builder.add_edge("ItenaryGenerator", "ValidateItenary")

        # Validation branch: pass or regenerate
        self.graph_builder.add_conditional_edges(
            "ValidateItenary",
            lambda state: state.get("validation_result", ""),
            {
                "PASS": END,
                "FAIL": "ItenaryGenerator"
            }
        )

        #Compile Graph
        return self.graph_builder.compile()
