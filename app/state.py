from typing import Optional, List, Dict, Any, Annotated
from typing_extensions import TypedDict
import operator

class AgentState(TypedDict):
    query: str
    next_step: Optional[str]
    sql_query: Optional[str]
    sql_data: Optional[List[Dict[str, Any]]]
    sql_error: Optional[str]
    retry_count: int
    analysis_result: Optional[str]
    visualization_spec: Optional[str]
    messages: Annotated[List[str], operator.add]
