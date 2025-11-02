from src.State.state import State
from src.fine_tuning.llm_tuning import Groqllm
from src.Tools.tool_assembly import Tools
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

class ItineraryNode:
    """
    Itinerary Node:
    - Takes a structured query (source, destination, dates, budget, travellers)
    - Generates a detailed structured itinerary in JSON format
    - Uses tools (web search + hotel rate fetcher) for realistic details
    """

    def __init__(self):
        # Initialize LLM
        groq_instance = Groqllm()
        groq_instance.load_data()
        self.llm = groq_instance.get_llm()

        # Attach tools
        self.tools = Tools.get_tools()
        self.tool_node = Tools.create_tool_node(self.tools)

    def process(self, state: State) -> dict:
      structured_query = state.get("structured_query")
      if not structured_query:
          raise ValueError("structured_query is missing in state")

      # --- ChatPromptTemplate ---
      prompt_template = ChatPromptTemplate.from_messages([
          HumanMessage(content="""
      You are a travel itinerary planner. Using the structured query below, create a realistic and helpful trip itinerary.
      Use web search and hotel tools where needed to find relevant options.

      Structured Query:
      {structured_query}

      Follow this exact output JSON structure (do not copy example values, use descriptive types):
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
              "avg_cost_per_person": "integer in ₹",
              "travel_time_est": "time duration",
              "pros": "advantages",
              "cons": "disadvantages",
              "source": "reference info or tool name"
            }
          ]
        },
        "StayOptions": {
          "choices": [
            {
              "name": "Hotel or hostel name",
              "approx_price_per_night_per_person": "integer in ₹",
              "facilities": "key features",
              "distance_from_center": "location info",
              "why_student_friendly": "reason",
              "live_example_source": "data source"
            }
          ]
        },
        "FoodSuggestions": {
          "avg_cost_per_meal_budget": "string like ₹100",
          "cheap_options": ["list", "of", "budget", "meals"],
          "must_try_local_dishes": ["dish1", "dish2"]
        },
        "DayWiseItinerary": {
          "Day1": {
            "route": "travel route or location",
            "transport_est_cost": "integer in ₹",
            "activities": ["activity1", "activity2"],
            "stay": "where to stay"
          }
        }
      }

      Rules:
      - Always output valid JSON.
      - Give multiple travel options and FoodSuggestions.
      - Do not include explanations or reasoning.
      - Use tool results for prices or hotel examples if available.
      - Focus on student-friendly, budget-conscious options.
      """)
      ])

      # --- Format prompt to string for LLM ---
      formatted_prompt_str = prompt_template.format(structured_query=structured_query)

      # --- Invoke LLM with tools ---
      itinerary_output = self.llm.invoke(formatted_prompt_str, tools=self.tools)

      # Merge output into state
      return {**state, "itenary": itinerary_output}

