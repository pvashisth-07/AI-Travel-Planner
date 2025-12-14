from src.fine_tuning.llm_tuning import Groqllm
from src.Graph.graph_builder import GraphBuilder
from langchain.schema import HumanMessage
import json


def get_user_input():
    print("\nEnter travel details:\n")

    source = input("Source city: ")
    destination = input("Destination city: ")
    start_date = input("Start date (YYYY-MM-DD): ")
    end_date = input("End date (YYYY-MM-DD): ")
    budget = input("Total budget (e.g., ₹10000): ")
    no_of_travellers = int(input("Number of travellers: "))

    return {
        "source": source,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "no_of_travellers": no_of_travellers
    }


def main():
    print("Initializing LLM...")
    llm = Groqllm().get_llm()
    print("LLM initialized successfully!")

    print("Building AI Travel Planner Graph...")
    graph = GraphBuilder(model=llm).ai_traveller_planner_graph()

    structured_query = get_user_input()

    initial_state = {
        "structured_query": structured_query,
        "graded_query": "PASS",   # ✅ skip QueryGenerator
        "messages": [
            HumanMessage(
                content=f"Generate travel itinerary for: {json.dumps(structured_query)}"
            )
        ]
    }

    print("\nRunning the LangGraph pipeline...")
    final_state = graph.invoke(initial_state)

    print("\n--- Final JSON Output ---")
    print(json.dumps(final_state["itinerary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
