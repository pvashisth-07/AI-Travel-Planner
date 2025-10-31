from src.fine_tuning.llm_tuning import Groqllm
from src.State.state import State
from src.Tools.tool_assembly import Tools


class ItenaryNode:
    """
    Itinerary Node:
    - Takes a structured query (source, destination, dates, budget, travellers)
    - Generates a detailed structured itinerary in JSON format
    - Uses tools (web search + hotel rate fetcher) for realistic details
    """

    def __init__(self):
        # Initialize LLM
        self.llm = Groqllm.get_llm()

        # Attach tools
        self.tools = Tools.get_tools()
        self.tool_node = Tools.create_tool_node(self.tools)

    def process(self, state: State) -> dict:
        """
        Process the input state and generate an itinerary response.
        """
        structured_query = state["structured_query"]

        # --- Itinerary format prompt ---
        prompt = f"""
        You are a travel itinerary planner. 
        Using the structured query below, create a realistic and helpful trip itinerary.
        Use web search and hotel tools where needed to find relevant options.

        Structured Query:
        {structured_query}

        Follow this **exact output JSON structure** (this is a format guide — do not copy data):
        {{
          "TripPlan": {{
            "title": "Short descriptive title (e.g., 4-Day Budget Himachal Trip)",
            "dates_assumed": "duration or date range",
            "group_size_assumed": "approximate traveler group",
            "notes": "short context summary"
          }},
          "TransportOptions": {{
            "comparison_table": [
              {{
                "mode": "Mode of travel (e.g., Train, Bus, Flight)",
                "avg_cost_per_person": int,
                "travel_time_est": "time duration",
                "pros": "advantages",
                "cons": "disadvantages",
                "source": "reference info or tool name"
              }}
            ]
          }},
          "StayOptions": {{
            "choices": [
              {{
                "name": "Hotel or hostel name",
                "approx_price_per_night_per_person": int,
                "facilities": "key features",
                "distance_from_center": "location info",
                "why_student_friendly": "reason",
                "live_example_source": "data source"
              }}
            ]
          }},
          "FoodSuggestions": {{
            "avg_cost_per_meal_budget": "string like ₹100",
            "cheap_options": ["list", "of", "budget", "meals"],
            "must_try_local_dishes": ["dish1", "dish2"]
          }},
          "DayWiseItinerary": {{
            "Day1": {{
              "route": "travel route or location",
              "transport_est_cost": int,
              "activities": ["activity1", "activity2"],
              "stay": "where to stay"
            }}
          }}
        }}

        Rules:
        - Always output valid JSON.
        - Give mutiple travel options and FoodSuggestions.
        - Do not include explanations or reasoning.
        - Do not copy the example values.
        - Use tool results for prices or hotel examples if available.
        """

        # Invoke LLM with tools enabled
        itinerary_output = self.llm.invoke(prompt, tools=self.tools)

        return {"itenary": itinerary_output}
