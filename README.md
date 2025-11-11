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

