from src.State.state import State
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


class Validate_Itinerary_Node:
    """
    Validate Itinerary Node:
    - Checks if generated itinerary matches required structure.
    - Returns only PASS or FAIL.
    """

    def __init__(self):
        load_dotenv()
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(api_key=self.groq_api_key, model="openai/gpt-oss-20b")

    def process(self, state: State) -> dict:
        """
        Validate the itinerary JSON format and return only PASS or FAIL.
        """
        generated_itenary = state["itinerary"]

        prompt = f"""
        You are a strict JSON structure validator.

        Check if the following itinerary strictly matches this structure:
        {{
          "TripPlan": {{
            "title": str,
            "dates_assumed": str,
            "group_size_assumed": str,
            "notes": str
          }},
          "TransportOptions": {{
            "comparison_table": [{{"mode": str, "avg_cost_per_person": int, "travel_time_est": str, "pros": str, "cons": str, "source": str}}]
          }},
          "StayOptions": {{
            "choices": [{{"name": str, "approx_price_per_night_per_person": int, "facilities": str, "distance_from_center": str, "why_student_friendly": str, "live_example_source": str}}]
          }},
          "FoodSuggestions": {{
            "avg_cost_per_meal_budget": str,
            "cheap_options": list,
            "must_try_local_dishes": list
          }},
          "DayWiseItinerary": {{
            "Day1": {{"route": str, "transport_est_cost": int, "activities": list, "stay": str}}
          }}
        }}

        The JSON must include all above top-level keys, and subfields should follow correct types.

        Itinerary to validate:
        {json.dumps(generated_itenary, indent=2)}

        If valid, output exactly:
        PASS

        If invalid or incomplete, output exactly:
        FAIL
        """

        response = self.llm.invoke(prompt)

        # Normalize output — keep only PASS or FAIL
        result = response.content.strip().upper()
        if "PASS" in result:
            result = "PASS"
        else:
            result = "FAIL"

        return {**state, "validation_result": result}
