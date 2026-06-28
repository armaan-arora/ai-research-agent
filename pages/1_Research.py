import streamlit as st
from src.graph import build_graph
from src.pdf_exporter import generate_pdf
from src.history import save_to_history
from datetime import datetime
import os

st.set_page_config(page_title="Research — AI Agent", page_icon="🔍", layout="wide")

st.title("🔍 Research Agent")
st.markdown("Enter any topic and the AI will research it and generate a structured report.")

topic = st.text_input("Research Topic", placeholder="e.g. AI in healthcare")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first!")
    else:
        graph = build_graph()
        status = st.empty()
        progress_bar = st.progress(0, text="Starting research...")
        progress = st.container()

        steps = {
            "planner": 0.2,
            "searcher": 0.4,
            "reflector": 0.6,
            "reporter": 0.8,
            "evaluator": 1.0
        }

        report = None
        evaluation = {}

        with progress:
            for event in graph.stream({"topic": topic, "loop_count": 0}):
                for node_name, node_output in event.items():

                    if node_name == "planner":
                        queries = node_output.get("sub_queries", [])
                        progress_bar.progress(steps["planner"], text="Step 1/5 — Planner thinking...")
                        status.success(f"✅ Planner completed — generated {len(queries)} queries")
                        with st.expander("See queries"):
                            for q in queries:
                                st.write(f"- {q}")

                    elif node_name == "searcher":
                        results = node_output.get("search_results", [])
                        progress_bar.progress(steps["searcher"], text="Step 2/5 — Searching the web...")
                        status.success(f"✅ Searcher completed — found {len(results)} results")

                    elif node_name == "reflector":
                        notes = node_output.get("reflection_notes", "")
                        loop = node_output.get("loop_count", 0)
                        progress_bar.progress(steps["reflector"], text="Step 3/5 — Reflector checking quality...")
                        if notes and notes.lower() != "none":
                            status.warning(f"🔄 Reflector — gaps found, searching again... (loop {loop})")
                            progress_bar.progress(steps["searcher"], text=f"Re-searching to fill gaps... (loop {loop})")
                        else:
                            status.success(f"✅ Reflector — sufficient info found!")

                    elif node_name == "reporter":
                        report = node_output.get("report", "")
                        progress_bar.progress(steps["reporter"], text="Step 4/5 — Writing report...")
                        status.success("✅ Reporter completed — report ready!")

                    elif node_name == "evaluator":
                        evaluation = node_output.get("evaluation", {})
                        progress_bar.progress(steps["evaluator"], text="Step 5/5 — Evaluating report quality...")
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

        progress_bar.empty()

        if report:
            st.markdown("---")
            st.markdown(report)

            save_to_history(topic, report, evaluation)

            os.makedirs("reports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/{topic.replace(' ', '_')}_{timestamp}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Research Report: {topic}\n\n")
                f.write(report)

            st.info(f"Report saved to: {filename}")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="⬇️ Download Markdown",
                    data=report,
                    file_name=f"{topic.replace(' ', '_')}_report.md",
                    mime="text/markdown"
                )
            with col2:
                pdf_buffer = generate_pdf(topic, report, evaluation)
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_buffer,
                    file_name=f"{topic.replace(' ', '_')}_report.pdf",
                    mime="application/pdf"
                )