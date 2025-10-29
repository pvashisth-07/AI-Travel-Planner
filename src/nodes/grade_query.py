from src.State.state import State
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

class GradeQuery:
    """
    GradeQuery Node — checks if the generated query matches the required structured format.
    """

    def __init__(self):
        load_dotenv()
        self.llm = ChatGroq(api_key=self.groq_api_key, model="openai/gpt-oss-20b")

    def process(self, state: State) -> dict:
        """
        Process the input state and evaluate if the query is properly structured.
        """

        user_query = state["structured_query"] if "structured_query" in state else state["query"]

        prompt = f"""
        You are a strict validator.

        Task:
        Check if the following query is a *structured query* following exactly this format:

        {{
            "source": str,
            "destination": str,
            "start_date": str,
            "end_date": str,
            "budget": str,
            "no_of_travellers": int
        }}

        - All keys must exist.
        - The data types must match.
        - "no_of_travellers" must be an integer.
        - If all fields are valid → Output exactly: "PASS"
        - If any field is missing or invalid → Output exactly: "FAIL"
          followed by a brief reason (e.g., Missing field 'budget').

        Query to check:
        {json.dumps(user_query, indent=4)}
        """

        response = self.llm.invoke(prompt)

        # Post-process response
        graded_output = response.strip()

        return {"graded_query": graded_output}
