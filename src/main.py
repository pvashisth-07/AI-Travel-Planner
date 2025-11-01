from src.fine_tuning.llm_tuning import Groqllm
from src.Graph.graph_builder import GraphBuilder
from src.State.state import State


def main():
    
    print("Initializing LLM...")
    groq_llm = Groqllm()       
    groq_llm.load_data()       
    llm = groq_llm.get_llm()   
    print("LLM initialized successfully!")   

    # Build the graph
    print("Building AI Travel Planner Graph...")
    graph = GraphBuilder(model=llm).ai_traveller_planner_graph()

    #Define initial state
    initial_state = State({
        "query": "Plan a 4-day trip from Delhi to Manali under ₹10,000 for two people starting next weekend."
    })

    #Run the graph
    print("Running the LangGraph pipeline...")
    final_state = graph.invoke(initial_state)

    #Display results
    print("\n--- Final Graph Output ---")
    for key, value in final_state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
