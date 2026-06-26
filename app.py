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
        graph = build_graph()

        # status container — shows live agent updates
        status = st.empty()
        progress = st.container()

        report = None

        with progress:
            for event in graph.stream({"topic": topic, "loop_count": 0}):
                for node_name, node_output in event.items():

                    if node_name == "planner":
                        queries = node_output.get("sub_queries", [])
                        status.success(f"✅ Planner completed — generated {len(queries)} queries")
                        with st.expander("See queries"):
                            for q in queries:
                                st.write(f"- {q}")

                    elif node_name == "searcher":
                        results = node_output.get("search_results", [])
                        status.success(f"✅ Searcher completed — found {len(results)} results")

                    elif node_name == "reflector":
                        notes = node_output.get("reflection_notes", "")
                        loop = node_output.get("loop_count", 0)
                        if notes and notes.lower() != "none":
                            status.warning(f"🔄 Reflector — gaps found, searching again... (loop {loop})")
                        else:
                            status.success(f"✅ Reflector — sufficient info found!")

                    elif node_name == "reporter":
                        report = node_output.get("report", "")
                        status.success("✅ Reporter completed — report ready!")

        if report:
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

            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name=f"{topic.replace(' ', '_')}_report.md",
                mime="text/markdown"
            )