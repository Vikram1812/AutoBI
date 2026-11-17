import json
import pandas as pd
import plotly.express as px
from typing import List, Dict, Any, Optional

def generate_plotly_spec(data: List[Dict[str, Any]], chart_type: str = "bar", x: str = None, y: str = None, title: str = "") -> Optional[str]:
    """Generates a serialized Plotly JSON specification from tabular records."""
    if not data:
        return None
        
    df = pd.DataFrame(data)
    if df.empty:
        return None

    # Handle Case: Single-row aggregate output (e.g., total_revenue vs total_profit)
    if len(df) == 1:
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if len(num_cols) >= 2:
            melted = df.melt(value_vars=num_cols, var_name="Metric", value_name="Amount")
            # Format clean metric names
            melted["Metric"] = melted["Metric"].str.replace("_", " ").str.title()
            fig = px.bar(
                melted, 
                x="Metric", 
                y="Amount", 
                color="Metric",
                text_auto=".2f",
                title=title or "Revenue vs Profit Comparison",
                template="plotly_dark"
            )
            return fig.to_json()

    # Handle Standard Multi-row Data
    if not x or not y or x not in df.columns or y not in df.columns:
        # Fallback auto-detection if columns are invalid
        cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if cat_cols and num_cols:
            x, y = cat_cols[0], num_cols[0]
        else:
            return None

    chart_type = (chart_type or "bar").lower()
    if chart_type == "bar":
        fig = px.bar(df, x=x, y=y, title=title, template="plotly_dark")
    elif chart_type == "line":
        fig = px.line(df, x=x, y=y, title=title, markers=True, template="plotly_dark")
    elif chart_type == "scatter":
        fig = px.scatter(df, x=x, y=y, title=title, template="plotly_dark")
    elif chart_type == "pie":
        fig = px.pie(df, names=x, values=y, title=title, template="plotly_dark")
    else:
        fig = px.bar(df, x=x, y=y, title=title, template="plotly_dark")
        
    return fig.to_json()