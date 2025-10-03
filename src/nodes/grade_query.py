from src.State.state import State
from src.fine_tuning.llm_tuning import Groqllm
class GradeQuery:
    """
    Grade Query Node implementation
    """

    def __init__(self):
        self.llm=Groqllm.get_llm()

    def process(self,state:State)->dict:
        """
        Process the input state and generate a graded query response.
        """

        return {"graded_query":self.llm.invoke(state["query"])}