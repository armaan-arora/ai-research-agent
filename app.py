import streamlit as st

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="wide"
)

# ─── HERO ───
st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 3.5rem;">🔍 AI Research Agent</h1>
        <p style="font-size: 1.3rem; color: gray;">
            Autonomous multi-agent research pipeline powered by GPT-4o-mini
        </p>
    </div>
""", unsafe_allow_html=True)

# ─── AGENT PIPELINE ───
st.markdown("### ⚙️ How it works")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div style="text-align:center; padding:1rem; background:#1e1e2e; border-radius:10px;">
        <div style="font-size:2rem;">🧠</div>
        <b>Planner</b>
        <p style="font-size:0.8rem; color:gray;">Breaks topic into focused sub-queries</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align:center; padding:1rem; background:#1e1e2e; border-radius:10px;">
        <div style="font-size:2rem;">🔎</div>
        <b>Searcher</b>
        <p style="font-size:0.8rem; color:gray;">Parallel web search + RAG cache</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align:center; padding:1rem; background:#1e1e2e; border-radius:10px;">
        <div style="font-size:2rem;">🔄</div>
        <b>Reflector</b>
        <p style="font-size:0.8rem; color:gray;">Self-checks and re-searches gaps</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="text-align:center; padding:1rem; background:#1e1e2e; border-radius:10px;">
        <div style="font-size:2rem;">📝</div>
        <b>Reporter</b>
        <p style="font-size:0.8rem; color:gray;">Writes structured report</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div style="text-align:center; padding:1rem; background:#1e1e2e; border-radius:10px;">
        <div style="font-size:2rem;">📊</div>
        <b>Evaluator</b>
        <p style="font-size:0.8rem; color:gray;">Scores report quality</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─── TECH STACK ───
st.markdown("### 🚀 Powered by")
c1, c2, c3, c4 = st.columns(4)
c1.metric("LLM", "GPT-4o-mini")
c2.metric("Search", "Tavily API")
c3.metric("Memory", "ChromaDB")
c4.metric("Framework", "LangGraph")

st.markdown("---")

# ─── FEATURES ───
st.markdown("### ✨ Features")
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    **🔄 Self Correction**
    Reflector agent identifies gaps and automatically re-searches until satisfied
    
    **⚡ Parallel Search**
    asyncio runs all sub-queries simultaneously — 3x faster than sequential
    """)

with f2:
    st.markdown("""
    **🧠 RAG Memory**
    ChromaDB caches results semantically — similar queries skip web search
    
    **📊 Quality Scoring**
    Every report scored across coverage, citations, clarity and depth
    """)

with f3:
    st.markdown("""
    **💾 Research History**
    SQLite powered persistent history with one-click report reload
    
    **📄 Export Options**
    Download reports as Markdown or PDF with one click
    """)

st.markdown("---")

# ─── CTA ───
st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h3>Ready to research?</h3>
        <p style="color: gray;">Click <b>Research</b> in the sidebar to get started</p>
    </div>
""", unsafe_allow_html=True)


