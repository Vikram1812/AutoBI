import json
import re
from app.llm import get_local_llm
from app.state import AgentState
from app.tools.viz_tools import generate_plotly_spec

ANALYST_PROMPT = """You are an Expert Data Analyst.
Review the user query and the retrieved database records.
Provide two things in valid JSON format:
1. "analysis": A clear, concise statistical interpretation answering the user query.
2. "visualization": Recommended chart configuration. If no chart makes sense, set to null.
   Format: {{"chart_type": "bar" | "line" | "scatter" | "pie", "x": "<column_name>", "y": "<column_name>", "title": "<chart_title>"}}

Output JSON format:
{{
  "analysis": "...",
  "visualization": {{"chart_type": "bar", "x": "category", "y": "total_revenue", "title": "Revenue by Category"}}
}}
"""

def analyst_node(state: AgentState) -> dict:
    llm = get_local_llm(temperature=0.1)
    query = state["query"]
    sql_data = state.get("sql_data", [])
    sql_query = state.get("sql_query", "")

    if not sql_data:
        return {
            "analysis_result": "No records matched your criteria or an error occurred during retrieval.",
            "visualization_spec": None,
            "messages": ["Data analyst found empty records."]
        }

    preview = json.dumps(sql_data[:20], indent=2)
    prompt = f"{ANALYST_PROMPT}\n\nUser Request: {query}\nExecuted SQL: {sql_query}\nQuery Output Records:\n{preview}\n\nJSON Output:"
    
    response = llm.invoke(prompt).content.strip()
    clean_json = re.sub(r"^```(json)?|```$", "", response, flags=re.MULTILINE).strip()
    
    viz_spec = None
    try:
        parsed = json.loads(clean_json)
        analysis_text = parsed.get("analysis", "Analysis completed.")
        viz_config = parsed.get("visualization")
        if viz_config and isinstance(viz_config, dict):
            viz_spec = generate_plotly_spec(
                data=sql_data,
                chart_type=viz_config.get("chart_type", "bar"),
                x=viz_config.get("x"),
                y=viz_config.get("y"),
                title=viz_config.get("title", "")
            )
    except Exception:
        analysis_text = response

    return {
        "analysis_result": analysis_text,
        "visualization_spec": viz_spec,
        "messages": ["Data analyst completed insights synthesis."]
    }
