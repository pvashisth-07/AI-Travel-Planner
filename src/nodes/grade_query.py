from src.State.state import State
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
class GradeQuery:
    """
    Grade Query Node implementation
    """

    def __init__(self):
        load_dotenv()
        self.llm=ChatGroq(api_key=self.groq_api_key,model="openai/gpt-oss-20b")

    def process(self,state:State)->dict:
        """
        Process the input state and generate a graded query response.
        """

        return {"graded_query":self.llm.invoke(state["query"])}