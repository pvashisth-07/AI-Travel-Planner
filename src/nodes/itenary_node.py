from src.fine_tuning.llm_tuning import Groqllm
from src.State.state import State
from src.Tools.tool_assembly import Tools
class ItenaryNode:
    """
    Itenary Node implementation
    """

    def __init__(self):
        self.llm=Groqllm.get_llm()

    def process(self,state:State)->dict:
        """
        Process the input state and generate an itenary response.
        """
        final_query=state['structured_query']
        

        return {"itenary":self.llm.invoke(state["query"])}