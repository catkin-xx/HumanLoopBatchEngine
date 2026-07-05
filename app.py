"""
PromptMill — Web Interface (Streamlit)
=======================================
Browser-based GUI for non-technical users.
"""
import streamlit as st
import json
from run_engine import HumanLoopBatchEngine, my_llm, TOTAL_COUNT

st.set_page_config(page_title="PromptMill", layout="wide")
st.title("🏭 Catkin")
st.caption("You set the standard. AI produces the sample. You approve. Batch done.")

if "engine" not in st.session_state:
    st.session_state.engine = HumanLoopBatchEngine(llm_call_func=my_llm, total_count=TOTAL_COUNT)
if "state" not in st.session_state:
    st.session_state.state = "init"

engine = st.session_state.engine

def reset():
    st.session_state.engine = HumanLoopBatchEngine(llm_call_func=my_llm, total_count=TOTAL_COUNT)
    st.session_state.state = "init"

# Step 1: Enter instruction
if st.session_state.state == "init":
    st.subheader("Step 1: Describe Your Task")
    instruction = st.text_area(
        "What do you want to generate?",
        height=150,
        placeholder="e.g., Write 10 Xiaohongshu-style product highlights for a smart toothbrush..."
    )
    if st.button("🚀 Generate Sample", type="primary"):
        if instruction.strip():
            with st.spinner("Generating sample..."):
                try:
                    engine.submit_instruction(instruction)
                    st.session_state.state = "review"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter an instruction.")

# Step 2: Review sample
if st.session_state.state == "review":
    st.subheader("Step 2: Review the Sample")
    st.info(engine.current_sample)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Satisfied — Batch Produce All", type="primary"):
            with st.spinner("Batch generating..."):
                engine.review_sample(approved=True)
            st.session_state.state = "done"
            st.rerun()

    with col2:
        new_instruction = st.text_area("Not satisfied? Revise your instruction:", height=100)
        if st.button("✏️ Regenerate with New Instruction"):
            if new_instruction.strip():
                with st.spinner("Regenerating..."):
                    engine.review_sample(approved=False, new_instruction=new_instruction)
                st.rerun()
            else:
                st.warning("Please enter the revised instruction.")

# Step 3: Download
if st.session_state.state == "done":
    st.subheader("🎉 Batch Complete")
    st.success(f"{len(engine.results)} items generated.")
    st.download_button(
        label="📥 Download Results (JSON)",
        data=json.dumps(engine.results, ensure_ascii=False, indent=2),
        file_name="output_results.json",
        mime="application/json",
        type="primary"
    )
    if st.button("🔄 Start New Task"):
        reset()
        st.rerun()
