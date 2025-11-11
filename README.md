# 🌍 AI Travel Planner — Intelligent Itinerary Generator ✈️
> 🚀 *An end-to-end AI-powered travel planner that converts natural-language trip requests into fully structured, budget-friendly itineraries using Groq’s LLM and LangGraph.*
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange) ![Groq-LLM](https://img.shields.io/badge/Groq-LLM-red) ![Status](https://img.shields.io/badge/Status-Active-success)

## 🧠 Overview
**AI Travel Planner** is an intelligent system that autonomously plans trips using **Large Language Models (LLMs)** and **LangGraph-based workflow orchestration**. It converts queries like:  
> *“Plan a 4-day budget trip from Delhi to Jaipur for 2 people under ₹10,000.”*  
into complete, validated itineraries — including transport, stays, meals, and day-wise activities.

## ⚙️ Tech Stack
| Layer | Technology Used |
|-------|------------------|
| 🧩 Core Framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| 🧠 LLM | [Groq LLM (`openai/gpt-oss-20b`)](https://groq.com) |
| 🧰 Prompt Orchestration | [LangChain](https://www.langchain.com) |
| 🔍 Search Integration | [Tavily Search API](https://tavily.com) |
| 🏨 Hotel Data | [Xotelo API](https://xotelo.com/api) |
| 🧾 Environment Management | `python-dotenv` |
| 💻 Language | Python 3.10+ |

## 🗺️ Workflow Architecture
User Query
↓
Query Generator ──▶ Grade Query
│ │
│ (PASS / FAIL)
│ ↓
└────────────▶ Itinerary Node ──▶ Validate Itinerary ──▶ (PASS → END / FAIL → Regenerate)

### 🔍 Node Responsibilities
| Node | Description |
|------|--------------|
| 🏁 **QueryGenerator** | Converts raw user query into structured JSON |
| ✅ **GradeQuery** | Validates structure and required fields |
| 🧳 **ItineraryNode** | Generates day-wise travel itinerary using LLM |
| 🔎 **Validate_Itinerary_Node** | Checks if itinerary format matches JSON schema |
| 🧰 **Tools** | Provides APIs for hotels & live web data |

## 🧩 Project Structure
AI_TRAVEL_PLANNER/
├── src/
│ ├── main.py # Entry point for graph execution
│ ├── Graph/
│ │ └── graph_builder.py # Builds LangGraph workflow
│ ├── State/
│ │ └── state.py # Shared state definition
│ ├── fine_tuning/
│ │ └── llm_tuning.py # LLM wrapper (Groq initialization)
│ ├── nodes/
│ │ ├── query_generator.py
│ │ ├── grade_query.py
│ │ ├── itinerary_node.py
│ │ └── validate_itinerary_node.py
│ └── Tools/
│ ├── tool_assembly.py
│ ├── hotel_tool.py
│ └── search_tool.py
├── .env # API keys and secrets
├── requirements.txt
├── app.py # Lightweight launcher
└── README.md


## 🚀 Example Run
**Command**
python app.py

## 🔧 Setup Instructions

### 1️⃣ Clone the repository
git clone https://github.com/pranav-vashisth/AI_Travel_Planner.git
cd AI_Travel_Planner
python -m venv ai_planner
# Activate the environment
ai_planner\Scripts\activate   # on Windows
source ai_planner/bin/activate   # on Linux/Mac
pip install -r requirements.txt

##💡 Features

✅ Converts natural language trip queries into structured format
✅ Generates realistic, validated itineraries
✅ Integrates hotel & travel APIs
✅ Modular, scalable LangGraph workflow
✅ Easily extendable with new nodes

##💡 Future Enhancements

🌐 Real-time flight, weather, and map APIs

📅 Smart date parsing (“next weekend”, “after Diwali”)

🧭 Google Maps integration

🎨 Streamlit-based UI

🧠 Fine-tuned travel dataset for Indian regions
