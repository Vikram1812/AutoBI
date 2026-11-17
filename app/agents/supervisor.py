import json
import re
from app.llm import get_local_llm
from app.state import AgentState

SUPERVISOR_PROMPT = """You are the Supervisor Agent in an autonomous data analytics system.
Given a user query, determine the initial routing.
Available actions:
- "sql": Query requires fetching, filtering, or aggregating relational database records.
- "general": Query is purely conversational, informational, or greeting without database interaction.

Output strictly valid JSON with no markdown wrapping:
{"next_step": "sql"} or {"next_step": "general"}
"""

def supervisor_node(state: AgentState) -> dict:
    llm = get_local_llm(temperature=0.0)
    user_query = state["query"]
    
    prompt = f"{SUPERVISOR_PROMPT}\n\nUser query: {user_query}\nJSON output:"
    response = llm.invoke(prompt).content.strip()
    
    clean_json = re.sub(r"^```(json)?|```$", "", response, flags=re.MULTILINE).strip()
    try:
        data = json.loads(clean_json)
        next_step = data.get("next_step", "sql")
    except Exception:
        next_step = "sql"
        
    return {
        "next_step": next_step,
        "messages": [f"Supervisor routed query to: {next_step}"]
    }
