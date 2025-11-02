from src.fine_tuning.llm_tuning import Groqllm
from src.Graph.graph_builder import GraphBuilder
from src.State.state import State
from langchain.schema import HumanMessage

def main():
    
    print("Initializing LLM...")
    groq_llm = Groqllm()              
    llm = groq_llm.get_llm()
    print("LLM initialized successfully!")   

    # Build the graph
    print("Building AI Travel Planner Graph...")
    graph = GraphBuilder(model=llm).ai_traveller_planner_graph()

    #Define initial state
    initial_state = {
    "query": "Create a detailed 4-day budget travel plan for two people from Delhi to Manali starting next weekend, keeping the total budget under ₹10,000. Include transport, stay, food, and daily activities.",
    "messages": [HumanMessage(content="Create a detailed 4-day budget travel plan for two people from Delhi to Manali starting next weekend, keeping the total budget under ₹10,000. Include transport, stay, food, and daily activities.")]
    }

    #Run the graph
    print("Running the LangGraph pipeline...")
    final_state = graph.invoke(initial_state)

    #Display results
    print("\n--- Final Graph Output ---")
    for key, value in final_state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
