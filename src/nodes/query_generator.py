from src.State.state import State
import ast
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

class QueryGenerator:
    """
    Generate user input query into structured format.
    Input: Raw string from user.
    Output: Structured query output dictionary.
    {
        source: str,
        destination: str,
        start_date: str,
        end_date: str,
        budget: str,
        no_of_travellers: int
    }
    """
    def __init__(self):
        load_dotenv()
        self.llm=ChatGroq(api_key=self.groq_api_key,model="openai/gpt-oss-20b")
    def process(self, state: State) -> dict:
        """Transform user input query into structured format."""
        prompt = f"""
        Transform the following user input query into a structured format with the following fields:
        source, destination, start_date, end_date, budget, no_of_travellers.
        If any field is missing in the input, set its value to "unknown" or 1 for no_of_travellers.
        
        User Input: "{state['query']}"
        
        Output format:
        {{
            "source": str,
            "destination": str,
            "start_date": str,
            "end_date": str,
            "budget": str,
            "no_of_travellers": int
        }}
        """
        response = self.llm.invoke(prompt)
        
        # Assuming the LLM returns a JSON-like string, we can use eval safely here
        try:
            structured_query = ast.literal_eval(response)
            if not isinstance(structured_query, dict):
                raise ValueError("LLM response is not a dictionary")
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}")
        
        # Ensure all required fields are present
        required_fields = ["source", "destination", "start_date", "end_date", "budget", "no_of_travellers"]
        for field in required_fields:
            if field not in structured_query:
                structured_query[field] = "unknown" if field != "no_of_travellers" else 1

        return {"structured_query": structured_query}