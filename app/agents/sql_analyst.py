import re
from app.llm import get_local_llm
from app.state import AgentState
from app.tools.db_tools import get_db_schema, execute_query

SQL_PROMPT = """You are a Senior SQL Analyst. Write a valid, standard DuckDB SQL query to answer the user request.
Database Schema:
{schema}

Guidelines:
1. Output ONLY the raw SQL query. Do not include markdown ticks, explanations, or commentary.
2. Use standard DuckDB syntax (e.g., date functions, joins, aggregates).
3. If an error is provided below, carefully correct the SQL syntax or column names.
"""

def clean_sql(text: str) -> str:
    cleaned = re.sub(r"^```(sql)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    if ";" in cleaned:
        cleaned = cleaned.split(";")[0] + ";"
    return cleaned

def sql_node(state: AgentState) -> dict:
    llm = get_local_llm(temperature=0.0)
    schema = get_db_schema()
    query = state["query"]
    error = state.get("sql_error")
    prior_sql = state.get("sql_query")
    retry_count = state.get("retry_count", 0)

    prompt = SQL_PROMPT.format(schema=schema)
    prompt += f"\n\nUser Request: {query}"
    if error and prior_sql:
        prompt += f"\n\nPrevious Attempt: {prior_sql}\nExecution Error: {error}\nPlease fix the query."

    response = llm.invoke(prompt).content
    sql = clean_sql(response)

    data, exec_error = execute_query(sql)
    if exec_error:
        return {
            "sql_query": sql,
            "sql_data": None,
            "sql_error": exec_error,
            "retry_count": retry_count + 1,
            "messages": [f"SQL execution error (attempt {retry_count + 1}): {exec_error}"]
        }
    
    return {
        "sql_query": sql,
        "sql_data": data,
        "sql_error": None,
        "messages": [f"SQL query successfully executed: {sql}"]
    }
