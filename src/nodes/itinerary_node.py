# src/nodes/itinerary_node.py (replace process method with this)
import json
import re
from src.State.state import State
from src.fine_tuning.llm_tuning import Groqllm
from src.Tools.tool_assembly import Tools

class ItineraryNode:
    def __init__(self, llm=None):
        # Accept shared llm if passed; otherwise create one (temporary)
        if llm:
            self.llm = llm
        else:
            groq_instance = Groqllm()
            self.llm = groq_instance.get_llm()

        self.tools = Tools.get_tools()

    def process(self, state: State) -> dict:
        structured_query = state.get("structured_query")
        if not structured_query:
            raise ValueError("❌ 'structured_query' missing in state")

        # Normalise/ensure JSON string for the model
        sq_json = json.dumps(structured_query, ensure_ascii=False, indent=2)

        # --- Strict prompt ---
        prompt_str = f"""
You are an EXACT JSON-output travel itinerary generator. You MUST use only the values provided in the Structured Query below.
Do not change the destination, source, dates, budget, or number of travellers. Do not invent new destinations.
Respond with ONLY valid JSON and nothing else (no commentary, no ticks, no explanation).

Structured Query (use these exact values):
{sq_json}

Produce a realistic, student-friendly itinerary JSON using the following schema exactly:
{{
  "TripPlan": {{
    "title": "Short descriptive title",
    "dates_assumed": "duration or date range",
    "group_size_assumed": "approximate traveler group",
    "notes": "short context summary"
  }},
  "TransportOptions": {{
    "comparison_table": [
      {{
        "mode": "Mode of travel (Train, Bus, Flight, etc.)",
        "avg_cost_per_person": 0,
        "travel_time_est": "time duration",
        "pros": "advantages",
        "cons": "disadvantages",
        "source": "reference or tool"
      }}
    ]
  }},
  "StayOptions": {{
    "choices": [
      {{
        "name": "Hotel/Hostel name",
        "approx_price_per_night_per_person": 0,
        "facilities": "key features",
        "distance_from_center": "location info",
        "why_student_friendly": "reason",
        "live_example_source": "data source"
      }}
    ]
  }},
  "FoodSuggestions": {{
    "avg_cost_per_meal_budget": "e.g., ₹150",
    "cheap_options": ["list", "of", "budget", "meals"],
    "must_try_local_dishes": ["dish1", "dish2"]
  }},
  "DayWiseItinerary": {{
    "Day1": {{
      "route": "travel route or location",
      "transport_est_cost": 0,
      "activities": ["activity1", "activity2"],
      "stay": "where to stay"
    }}
  }}
}}

IMPORTANT: The "destination" in TripPlan and DayWiseItinerary must match the Structured Query 'destination' exactly.
"""

        # Debug print — remove or switch to logging once stable
        print("---- PROMPT SENT TO LLM ----")
        print(prompt_str)
        print("---- END PROMPT ----")

        # Invoke LLM with deterministic temperature when supported
        try:
            # ChatGroq SDK may accept model params; adapt if parameter name differs.
            response = self.llm.invoke(prompt_str, temperature=0.0)
        except TypeError:
            # If ChatGroq.invoke doesn't accept temperature param, call without it
            response = self.llm.invoke(prompt_str)

        # Debug: show raw response object
        print("---- RAW LLM RESPONSE ----")
        # try to be safe about extracting content
        if hasattr(response, "content"):
            raw_text = response.content
        else:
            raw_text = str(response)
        print(raw_text)
        print("---- END RAW ----")

        # --- Extract JSON robustly ---
        text = str(raw_text).strip()
        try:
            itinerary_json = json.loads(text)
        except json.JSONDecodeError:
            m = re.search(r"\{[\s\S]*\}", text)
            if m:
                try:
                    itinerary_json = json.loads(m.group())
                except Exception as e:
                    print("JSON extraction failed:", e)
                    itinerary_json = {"raw_output": text}
            else:
                itinerary_json = {"raw_output": text}

        # Optional check: ensure destination matches structured_query
        dest = structured_query.get("destination")
        # Defensive: check if itinerary contains the dest string anywhere; if not, attach a flag
        if dest and dest.lower() not in json.dumps(itinerary_json).lower():
            print(f"⚠️ Destination '{dest}' not found in generated itinerary! Marking for re-run.")
            # You can decide to force FAIL here by adding a flag or raising
            itinerary_json["_warning"] = f"Destination '{dest}' not found."

        return {**state, "itinerary": itinerary_json}
