# AutoBI: Autonomous Multi-Agent Analytics & SQL Pipeline

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![LM Studio](https://img.shields.io/badge/Inference-LM%20Studio%20(Local)-green.svg)](https://lmstudio.ai/)
[![DuckDB](https://img.shields.io/badge/Database-DuckDB-yellow.svg)](https://duckdb.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**AutoBI** is a privacy-first, fully local multi-agent data analytics platform. It translates natural language business questions into executable, self-healing SQL queries, executes statistical aggregations, and automatically generates interactive Plotly visualizations—powered entirely by open-weights LLMs hosted locally via LM Studio.

---

## Key Highlights

- **Supervisor Multi-Agent Coordination:** Orchestrated with LangGraph to classify user intent and route execution between specialized database and analytics agents.
- **Self-Healing Text-to-SQL:** Dynamically inspects DuckDB schemas and automatically enters an error-reflection loop to rectify syntax and column mismatches if a query execution fails.
- **100% Offline & Free Inference:** Connects to an OpenAI-compatible local server (`http://localhost:1234/v1`) using open models such as `Qwen2.5-Coder-7B-Instruct`—no cloud API keys, zero subscription costs, and complete data privacy.
- **Embedded In-Memory OLAP:** Leverages DuckDB for rapid analytical aggregation over structured relational tables.
- **Automated Visual Dashboards:** Serializes query results into interactive Plotly specifications displayed on the frontend.

---

## System Architecture

```text
                      +-----------------------------+
                      | User Prompt / Business Query|
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |     Supervisor Router       |
                      |   (LangGraph Orchestrator)  |
                      +--------------+--------------+
                                     |
        +----------------------------+----------------------------+
        |                                                         |
        v                                                         v
+--------------------------+                      +-----------------------------+
|    SQL Analyst Agent     |                      |     Data Analyst Agent      |
| - Introspects DDL Schema |                      | - Statistical summary       |
| - Generates DuckDB SQL   |                      | - Outlier & trend analysis  |
| - Self-Correction Loop   |                      | - In-memory transformations |
+-------------+------------+                      +--------------+--------------+
              |                                                  |
              +----------------------------+---------------------+
                                           |
                                           v
                             +---------------------------+
                             |   Visualization Server    |
                             |  - Generates Plotly Specs |
                             +-------------+-------------+
                                           |
                                           v
                             +---------------------------+
                             | Interactive UI / API      |
                             |  (FastAPI / Streamlit)    |
                             +---------------------------+
```

---

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Agent Orchestration** | LangGraph, LangChain-OpenAI | State machine, supervisor routing, recovery loops |
| **Local LLM Serving** | LM Studio (`localhost:1234`) | Local OpenAI-compatible REST server |
| **Target Model** | Qwen 2.5 Coder 7B Instruct (GGUF) | Text-to-SQL generation, Python scripting, routing |
| **Analytics Engine** | DuckDB, Pandas, NumPy | Embedded SQL database and tabular processing |
| **Visualizations** | Plotly Express / Graph Objects | Interactive chart generation and JSON serialization |
| **Backend & UI** | FastAPI, Uvicorn, Streamlit | REST API endpoints and dashboard UI |

---

## Project Structure

```text
autobi/
│
├── app/
│   ├── __init__.py
│   ├── llm.py              # LM Studio local client setup
│   ├── state.py            # LangGraph TypedDict state schema
│   ├── graph.py            # Workflow nodes and conditional edges
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── supervisor.py   # Intent classification & routing
│   │   ├── sql_analyst.py  # Text-to-SQL & syntax self-repair
│   │   └── data_analyst.py # Descriptive statistics & summaries
│   └── tools/
│       ├── db_tools.py     # DuckDB connection & schema introspection
│       └── viz_tools.py    # Plotly figure generator
│
├── data/
│   └── sample_data.duckdb  # Relational database file
│
├── app.py                  # Streamlit user interface
├── main.py                 # FastAPI backend entrypoint
├── requirements.txt        # Python package dependencies
└── README.md
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- [LM Studio](https://lmstudio.ai/) installed on your local machine

### 2. Configure LM Studio
1. Launch LM Studio and search for **`Qwen2.5-Coder-7B-Instruct-GGUF`** (recommended: `Q4_K_M` or `Q5_K_M`).
2. Navigate to the **Local Server** tab (`<->` on the left sidebar).
3. Select and load the model at the top.
4. Set the port to `1234`, enable **CORS**, and click **Start Server**.
5. Test that the endpoint is live by browsing to `http://localhost:1234/v1/models`.

### 3. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/autobi.git
cd autobi

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Running the Project

**Option A: Interactive Dashboard (Streamlit)**
```bash
streamlit run app.py
```

**Option B: REST API Service (FastAPI)**
```bash
uvicorn main:app --reload --port 8080
```
Interactive API documentation will be available at `http://localhost:8080/docs`.

---

## Example Usage

**Prompt:**
> *"Identify the top 5 product categories by total sales volume, compute their average order values, and visualize the comparison using a bar chart."*

**Pipeline Output:**
1. **Supervisor** categorizes request as SQL + Visualization.
2. **SQL Analyst** pulls table schemas, writes DuckDB SQL, verifies execution, and fetches tabular rows.
3. **Data Analyst** computes summary metrics and flags top revenue drivers.
4. **Visualizer** compiles an interactive Plotly bar chart rendered directly in the interface.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.