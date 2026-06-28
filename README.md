# AI Research Agent 🔍

A multi-agent AI research pipeline built with LangGraph and OpenAI that autonomously researches any topic and generates a structured report.

## Architecture

User Input → Planner → Searcher → Reflector → Reporter → Final Report

- **Planner** — breaks topic into focused sub-queries
- **Searcher** — fetches real-time web results using Tavily
- **Reflector** — self-checks for gaps and loops back if needed
- **Reporter** — generates structured markdown report

## Tech Stack

- LangGraph — multi-agent workflow orchestration
- OpenAI GPT-4o-mini — LLM for all agents
- Tavily — for real-time web search
- Pydantic — structured output validation
- Streamlit — web UI

## Setup

1. Clone the repo
git clone https://github.com/YOURUSERNAME/ai-research-agent.git
cd ai-research-agent

2. Create virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install langgraph langchain langchain-openai langchain-tavily python-dotenv streamlit pydantic

4. Add API keys — create a .env file
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key

5. Run the app
streamlit run app.py

## Features

- Multi-agent architecture with self-correction loop
- Real-time web search with Tavily
- Pydantic structured outputs — no fragile string parsing
- Streamlit UI with download button
- Auto-saves reports as markdown files
