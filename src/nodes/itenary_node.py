from src.State.state import State

class ItenaryNode:
    """
    Itenary Node implementation
    """

    def __init__(self,model):
        self.llm=model

    def process(self,state:State)->dict:
        """
        Process the input state and generate an itenary response.
        """

        return {"itenary":self.llm.invoke(state['messages'])}