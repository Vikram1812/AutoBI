import streamlit as st
import json
import plotly.io as pio
from app.graph import workflow

st.set_page_config(page_title="AutoBI - Local Multi-Agent Analytics", layout="wide")

st.title("AutoBI: Local Multi-Agent BI Engine")
st.caption("Powered by LangGraph + Local LM Studio + DuckDB + Plotly")

query = st.text_input(
    "Ask a business question about your data:",
    placeholder="e.g. Compare total revenue and average profit margin across product categories"
)

if st.button("Run Analytics", type="primary"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Multi-agent team analyzing data via LM Studio..."):
            initial_state = {
                "query": query,
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

        st.subheader("Analytical Insights")
        st.markdown(result.get("analysis_result") or "No textual synthesis generated.")

        # Display Visualization if generated
        spec = result.get("visualization_spec")
        if spec:
            st.subheader("Visual Dashboard")
            fig = pio.from_json(spec)
            st.plotly_chart(fig, use_container_width=True)

        # Technical Details Expander
        with st.expander("Inspected SQL & Underlying Execution"):
            st.code(result.get("sql_query") or "No SQL executed", language="sql")
            st.write("Execution Log:")
            for msg in result.get("messages", []):
                st.text(f"• {msg}")
            if result.get("sql_data"):
                st.write("Retrieved Rows:")
                st.dataframe(result.get("sql_data"))
