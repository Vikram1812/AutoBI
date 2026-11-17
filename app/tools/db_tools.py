import os
import duckdb
from typing import Tuple, List, Dict, Any, Optional

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "autobi.duckdb")
)

def get_db_schema() -> str:
    """Inspects tables and column DDL structures in DuckDB."""
    con = duckdb.connect(DB_PATH, read_only=True)
    tables = con.execute("SHOW TABLES").fetchall()
    schema_lines = []
    
    for (tbl,) in tables:
        cols = con.execute(f"DESCRIBE {tbl}").fetchall()
        col_defs = ", ".join([f"{col[0]} ({col[1]})" for col in cols])
        schema_lines.append(f"Table '{tbl}': {col_defs}")
    
    con.close()
    return "\n".join(schema_lines)

def execute_query(query: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Executes a DuckDB SQL query and returns row records or error string."""
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        df = con.execute(query).df()
        con.close()
        return df.to_dict(orient="records"), None
    except Exception as e:
        con.close()
        return None, str(e)
