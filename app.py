import streamlit as st
from src.graph import build_graph
from datetime import datetime
import os

st.set_page_config(page_title="AI Research Agent", page_icon="🔍", layout="wide")

st.title("🔍 AI Research Agent")
st.markdown("Enter any topic and the AI will research it and generate a structured report.")

topic = st.text_input("Research Topic", placeholder="e.g. AI in healthcare")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first!")
    else:
        with st.spinner("Researching... this may take 30-60 seconds"):
            graph = build_graph()
            result = graph.invoke({"topic": topic})
            report = result["report"]

        st.success("Report generated!")
        st.markdown("---")
        st.markdown(report)

        # save to file
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/{topic.replace(' ', '_')}_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Research Report: {topic}\n\n")
            f.write(report)

        st.info(f"Report saved to: {filename}")

        # download button
        st.download_button(
            label="Download Report",
            data=report,
            file_name=f"{topic.replace(' ', '_')}_report.md",
            mime="text/markdown"
        )