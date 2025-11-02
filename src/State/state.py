from typing_extensions import TypedDict
from typing import List
from langgraph.graph.message import add_messages
from typing import Annotated

class State(TypedDict, total=False):
    """
    Represent the structure of the state used in the graph.
    total=False → allows optional keys
    """
    messages: Annotated[List[str], add_messages]  # List of messages
    query: str                                    # Raw user query
    structured_query: dict                        # Generated structured query
    graded_query: str                             # PASS or FAIL from grading
    itenary: dict                                 # Generated itinerary
    validation_result: str                        # PASS or FAIL from itinerary validation
