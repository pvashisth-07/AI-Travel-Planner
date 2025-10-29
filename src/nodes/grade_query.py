from src.State.state import State
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

class GradeQuery:
    """
    GradeQuery Node — strictly checks if the generated query matches the required structured format.
    Returns only 'PASS' or 'FAIL'.
    """

    def __init__(self):
        load_dotenv()
        self.llm = ChatGroq(api_key=self.groq_api_key, model="openai/gpt-oss-20b")

    def process(self, state: State) -> dict:
        """
        Process the input state and return 'PASS' or 'FAIL' only.
        """

        user_query = state.get("structured_query", state.get("query", {}))

        prompt = f"""
        You are a strict validator.

        Check if the following query is a *structured query* that exactly follows this format:

        {{
            "source": str,
            "destination": str,
            "start_date": str,
            "end_date": str,
            "budget": str,
            "no_of_travellers": int
        }}

        - All keys must be present.
        - The data types must match.
        - "no_of_travellers" must be an integer.
        
        Output strictly one word:
        PASS  → if the query fully matches the required format
        FAIL  → otherwise

        Do not include any explanation, punctuation, or extra text.

        Query to check:
        {json.dumps(user_query, indent=4)}
        """

        response = self.llm.invoke(prompt)
        result = response.strip().upper()

        # Normalize the LLM output — force to only PASS or FAIL
        if "PASS" in result:
            result = "PASS"
        else:
            result = "FAIL"

        return {"graded_query": result}
