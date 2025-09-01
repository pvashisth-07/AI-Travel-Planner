import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
class Groqllm:
    def __init__(self):
        load_dotenv()

    def load_data(self, file_path="sample_data.json"):
        """Load training samples from JSON file"""
        with open(file_path, "r", encoding="utf-8") as f:
            self.samples = json.load(f)
    
    def get_llm(self):
        """Train llm on sample.json file and make it ready for use."""

        try:
            os.environ["GROQ_API_KEY"]=self.groq_api_key=os.getenv("GROQ_API_KEY")
            self.llm=ChatGroq(api_key=self.groq_api_key,model="openai/gpt-oss-20b")

            example_text = json.dumps(self.samples, indent=2)
            prompt=ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are an excellent **Budget Travel Itinerary Generator**.  
            Your task is to create **budget-friendly trip plans** specifically designed for **college students**.  

            ### Context:
            - You have been provided with a dataset of sample trips learn from it and make yourself ready to produce such itineraries:  
            {example_text}  

            ### Your Objectives:
            1. Carefully read and learn the style, structure, and cost ranges from the dataset.  
            2. Always produce trip plans in the **same JSON schema**, with these keys:
            - TripPlan  
            - TransportOptions  
            - StayOptions  
            - FoodSuggestions  
            - DayWiseItinerary  
            3. Ensure the output is **valid JSON only** (no explanations, no extra text).  
            4. Costs must be in **₹ INR**, realistic for student budgets.  
            5. Focus on **student-friendly transport, hostels/ashrams, local food, free or cheap activities**.  
            6. Day-wise itineraries should mix **spiritual, cultural, and adventure elements** where relevant.  
            7. Also make sure to include seasonal considerations in the trip plans.  

            ### Style:
            - Be concise, structured, and cost-conscious.  """),
                HumanMessage(content=example_text)
            ])

            self.model=prompt | self.llm
            
        except Exception as e:
            print(f"Error occurred with exception {e}")

        return self.model
