from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.graph import workflow

app = FastAPI(
    title="AutoBI API",
    description="Local Autonomous Multi-Agent Analytics & SQL Pipeline"
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    analysis: Optional[str]
    sql_query: Optional[str]
    sql_data: Optional[List[Dict[str, Any]]]
    visualization_spec: Optional[str]
    messages: List[str]

@app.post("/analyze", response_model=QueryResponse)
def analyze_data(req: QueryRequest):
    initial_state = {
        "query": req.query,
        "next_step": None,
        "sql_query": None,
        "sql_data": None,
        "sql_error": None,
        "retry_count": 0,
        "analysis_result": None,
        "visualization_spec": None,
        "messages": []
    }
    result = workflow.invoke(initial_state)
    return QueryResponse(
        query=req.query,
        analysis=result.get("analysis_result"),
        sql_query=result.get("sql_query"),
        sql_data=result.get("sql_data"),
        visualization_spec=result.get("visualization_spec"),
        messages=result.get("messages", [])
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
