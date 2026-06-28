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

                    elif node_name == "evaluator":
                        evaluation = node_output.get("evaluation", {})
                        status.success("✅ Evaluator completed — report scored!")

                        st.markdown("---")
                        st.subheader("📊 Report Quality Score")

                        col1, col2, col3, col4, col5 = st.columns(5)
                        col1.metric("Coverage", f"{evaluation.get('coverage')}/10")
                        col2.metric("Citations", f"{evaluation.get('citations')}/10")
                        col3.metric("Clarity", f"{evaluation.get('clarity')}/10")
                        col4.metric("Depth", f"{evaluation.get('depth')}/10")
                        col5.metric("Overall", f"{evaluation.get('overall')}/10")

                        st.info(f"💡 Feedback: {evaluation.get('feedback')}")

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