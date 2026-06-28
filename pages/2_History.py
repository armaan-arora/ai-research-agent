import streamlit as st
from src.history import load_history, clear_history
from src.pdf_exporter import generate_pdf

st.set_page_config(page_title="History — AI Agent", page_icon="📚", layout="wide")

st.title("📚 Research History")
st.markdown("All your past research sessions saved here.")

history = load_history()

if not history:
    st.info("No research history yet! Go to Research page to get started.")
else:
    if st.button("🗑️ Clear All History", type="secondary"):
        clear_history()
        st.rerun()

    st.markdown(f"**{len(history)} research sessions found**")
    st.markdown("---")

    for i, entry in enumerate(history):
        with st.expander(f"🔍 {entry['topic']} — {entry['timestamp']} — Score: {entry['overall_score']}/10"):
            
            # scores
            evaluation = entry.get("evaluation", {})
            if evaluation:
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Coverage", f"{evaluation.get('coverage', 'N/A')}/10")
                col2.metric("Citations", f"{evaluation.get('citations', 'N/A')}/10")
                col3.metric("Clarity", f"{evaluation.get('clarity', 'N/A')}/10")
                col4.metric("Depth", f"{evaluation.get('depth', 'N/A')}/10")
                col5.metric("Overall", f"{evaluation.get('overall', 'N/A')}/10")

            st.markdown("---")
            st.markdown(entry["report"])

            # download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="⬇️ Download Markdown",
                    data=entry["report"],
                    file_name=f"{entry['topic'].replace(' ', '_')}_report.md",
                    mime="text/markdown",
                    key=f"md_{i}"
                )
            with col2:
                pdf_buffer = generate_pdf(
                    entry["topic"],
                    entry["report"],
                    evaluation
                )
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_buffer,
                    file_name=f"{entry['topic'].replace(' ', '_')}_report.pdf",
                    mime="application/pdf",
                    key=f"pdf_{i}"
                )