from langgraph.graph import StateGraph, START, END
from app.state import AgentState
from app.agents.supervisor import supervisor_node
from app.agents.sql_analyst import sql_node
from app.agents.data_analyst import analyst_node

def supervisor_router(state: AgentState) -> str:
    return state.get("next_step", "sql")

def sql_reflection_router(state: AgentState) -> str:
    # If error and retries < 2, loop back to sql_analyst
    if state.get("sql_error") and state.get("retry_count", 0) < 2:
        return "retry"
    return "analyst"

builder = StateGraph(AgentState)

# Add Nodes
builder.add_node("supervisor", supervisor_node)
builder.add_node("sql_analyst", sql_node)
builder.add_node("data_analyst", analyst_node)

# Add Edges & Conditional Routing
builder.add_edge(START, "supervisor")
builder.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "sql": "sql_analyst",
        "general": END
    }
)

builder.add_conditional_edges(
    "sql_analyst",
    sql_reflection_router,
    {
        "retry": "sql_analyst",
        "analyst": "data_analyst"
    }
)

builder.add_edge("data_analyst", END)

# Compile Workflow Graph
workflow = builder.compile()
