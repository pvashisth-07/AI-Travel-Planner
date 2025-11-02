import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


class Groqllm:
    def __init__(self):
        load_dotenv()

    def get_llm(self):
        """Return a raw LLM instance for nodes to use with custom prompts."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")

        return ChatGroq(api_key=api_key, model="openai/gpt-oss-20b")
