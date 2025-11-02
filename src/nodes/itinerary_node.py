from src.State.state import State
from src.fine_tuning.llm_tuning import Groqllm
from src.Tools.tool_assembly import Tools
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
import json


class ItineraryNode:
    """
    Itinerary Node:
    - Takes a structured query (source, destination, dates, budget, travellers)
    - Generates a detailed structured itinerary in JSON format
    - Uses tools (web search + hotel rate fetcher) for realistic details
    """

    def __init__(self):
        # Initialize LLM from Groq wrapper (no prompt inside Groqllm)
        groq_instance = Groqllm()
        self.llm = groq_instance.get_llm()

        # Attach tools
        self.tools = Tools.get_tools()

    def process(self, state: State) -> dict:
        structured_query = state.get("structured_query")
        if not structured_query:
            raise ValueError("❌ 'structured_query' missing in state")

        # --- Define prompt ---
        prompt_template = ChatPromptTemplate.from_messages([
            HumanMessage(content="""
You are a travel itinerary planner.

Using the structured query below, create a realistic and budget-friendly trip itinerary for college students.

Structured Query:
{structured_query}

Follow this exact JSON output structure:
{
  "TripPlan": {
    "title": "Short descriptive title (e.g., 4-Day Budget Himachal Trip)",
    "dates_assumed": "duration or date range",
    "group_size_assumed": "approximate traveler group",
    "notes": "short context summary"
  },
  "TransportOptions": {
    "comparison_table": [
      {
        "mode": "Mode of travel (Train, Bus, Flight, etc.)",
        "avg_cost_per_person": 0,
        "travel_time_est": "time duration",
        "pros": "advantages",
        "cons": "disadvantages",
        "source": "reference or tool"
      }
    ]
  },
  "StayOptions": {
    "choices": [
      {
        "name": "Hotel/Hostel name",
        "approx_price_per_night_per_person": 0,
        "facilities": "key features",
        "distance_from_center": "location info",
        "why_student_friendly": "reason",
        "live_example_source": "data source"
      }
    ]
  },
  "FoodSuggestions": {
    "avg_cost_per_meal_budget": "e.g., ₹150",
    "cheap_options": ["list", "of", "budget", "meals"],
    "must_try_local_dishes": ["dish1", "dish2"]
  },
  "DayWiseItinerary": {
    "Day1": {
      "route": "travel route or location",
      "transport_est_cost": 0,
      "activities": ["activity1", "activity2"],
      "stay": "where to stay"
    }
  }
}

Rules:
- Always output VALID JSON only.
- Use realistic student-friendly pricing and stays.
- No explanations or text outside JSON.
- Use web/hotel tools for realistic data.
""")
        ])

        # Format the prompt with structured query
        formatted_prompt = prompt_template.format(structured_query=structured_query)

        # --- Invoke LLM ---
        response = self.llm.invoke(formatted_prompt)

        # --- Parse and clean output ---
        try:
            itinerary_json = json.loads(response.content)
        except json.JSONDecodeError:
            print("⚠️ Warning: Model did not return valid JSON. Returning raw response.")
            itinerary_json = {"raw_output": response}

        # --- Return only what this node updates ---
        return {**state,"itenary": itinerary_json}
