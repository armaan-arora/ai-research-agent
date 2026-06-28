# 🔍 AI Research Agent

An autonomous multi-agent research pipeline built with LangGraph and OpenAI that researches any topic, self-corrects its findings, and generates a structured report with quality scoring.

## 🎥 Demo

![Demo GIF](demo.gif)

## 🏗️ Architecture

```
User Input → Planner → Searcher → Reflector → Reporter → Evaluator
                           ↑            |
                           |  (if gaps) |
                           └────────────┘
```

### Agents
| Agent | Role |
|-------|------|
| 🧠 **Planner** | Breaks topic into 3 focused sub-queries using GPT-4o-mini |
| 🔎 **Searcher** | Runs parallel web searches via Tavily, checks RAG cache first |
| 🔄 **Reflector** | Self-checks research quality, loops back if gaps found |
| 📝 **Reporter** | Generates structured markdown report with citations |
| 📊 **Evaluator** | Scores report quality 1-10 across 4 dimensions |

## ✨ Features

- **Multi-agent orchestration** — LangGraph powered workflow with conditional routing
- **Self-correction loop** — Reflector agent identifies gaps and re-searches automatically
- **RAG memory** — ChromaDB caches search results semantically, skips API calls for similar queries
- **Parallel search** — asyncio runs all sub-queries simultaneously for 3x speed improvement
- **Pydantic structured outputs** — type-safe LLM responses, no fragile string parsing
- **Live streaming UI** — watch each agent work in real time with step-by-step progress bar
- **Quality scoring** — automated evaluation across coverage, citations, clarity and depth
- **Research history** — SQLite powered persistent history with full report reload
- **Export options** — download reports as Markdown or PDF with one click
- **Multipage UI** — clean homepage, dedicated research page and history page

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| LangGraph | Multi-agent workflow orchestration |
| OpenAI GPT-4o-mini | LLM for all agent reasoning |
| Tavily | Real-time web search API |
| ChromaDB | Vector database for RAG memory |
| Pydantic | Structured output validation |
| SQLite | Persistent research history |
| Streamlit | Interactive multipage web UI |
| asyncio | Parallel search execution |
| ReportLab | PDF report generation |

## 📁 Project Structure

```
ai-research-agent/
├── src/
│   ├── agents.py        # All 5 agent node functions
│   ├── graph.py         # LangGraph workflow definition
│   ├── schemas.py       # Pydantic output schemas
│   ├── tools.py         # Tavily search tool setup
│   ├── memory.py        # ChromaDB RAG memory
│   ├── history.py       # SQLite research history
│   └── pdf_exporter.py  # PDF generation with ReportLab
├── pages/
│   ├── 1_Research.py    # Research agent page
│   └── 2_History.py     # Research history page
├── app.py               # Homepage
├── main.py              # Terminal entry point
├── requirements.txt     # Python dependencies
└── .env                 # API keys (not committed)
```

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOURUSERNAME/ai-research-agent.git
cd ai-research-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API keys
Create a `.env` file in the root folder:
```
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 🔄 How It Works

1. **User enters a topic** — e.g. "AI in healthcare"
2. **Planner** breaks it into 3 focused sub-queries using GPT-4o-mini
3. **Searcher** checks RAG cache first, falls back to Tavily web search if needed
4. **Reflector** evaluates research quality — loops back to Searcher if gaps found
5. **Reporter** synthesizes all findings into a structured markdown report with citations
6. **Evaluator** scores the report across 4 quality dimensions
7. **User downloads** report as Markdown or PDF

## 💡 Key Design Decisions

**Why LangGraph?**
LangGraph supports conditional edges and cycles — essential for the Reflector's self-correction loop. Simple LangChain chains can't loop back to previous steps.

**Why Pydantic structured outputs?**
String parsing of LLM responses is fragile in production. Pydantic schemas enforce type safety at the API level using OpenAI's function calling under the hood — guaranteed structure every time.

**Why ChromaDB for RAG?**
Semantic caching with vector similarity means similar queries like "AI in medicine" and "artificial intelligence healthcare" both hit the cache — not just exact matches. Saves API costs and speeds up repeated research.

**Why asyncio for search?**
Sequential search for 3 queries takes ~9 seconds. Parallel search takes ~3 seconds. 3x faster with zero extra API cost.

**Why SQLite for history?**
SQLite is transaction-safe, supports SQL queries, and is more production-like than flat JSON file storage. History persists across app restarts and browser refreshes.

## 🔮 Future Improvements

- [ ] PostgreSQL for production-grade multi-user history storage
- [ ] FastAPI endpoint to expose research pipeline as REST API
- [ ] Source credibility scoring — rank sources by reliability
- [ ] Fact verification agent — cross-check facts across multiple sources
- [ ] Multi-language report generation
- [ ] Docker containerization for one-command deployment

## 📄 License

MIT License
