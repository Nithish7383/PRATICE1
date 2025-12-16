import streamlit as st
import shutil
from pathlib import Path

from service.risk_engine import run_engine
from ai.ollama_llm import OllamaLLM
from ai.release_risk_ai import ReleaseRiskAIEngine


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="SDLC Release Risk Analyzer",
    layout="wide"
)

st.title("AI-Assisted SDLC Release Risk Analyzer")
st.write("Predicts release risk using SDLC metrics and AI insights")

DATA_DIR = Path("app/data")
DATA_DIR.mkdir(exist_ok=True)

# -----------------------------
# FILE UPLOAD
# -----------------------------
st.subheader("Upload SDLC CSV Files")

test_file = st.file_uploader("Test Results CSV", type="csv")
commit_file = st.file_uploader("Commit Activity CSV", type="csv")
defect_file = st.file_uploader("Defects CSV", type="csv")
pipeline_file = st.file_uploader("Pipeline Runs CSV", type="csv")

if st.button("Analyze Release Risk"):
    if not all([test_file, commit_file, defect_file, pipeline_file]):
        st.error("Please upload all 4 CSV files")
        st.stop()

    # Save uploaded files
    files = {
        "test_results.csv": test_file,
        "commit_activity.csv": commit_file,
        "defects.csv": defect_file,
        "pipeline_runs.csv": pipeline_file,
    }

    for filename, uploaded_file in files.items():
        with open(DATA_DIR / filename, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

    # -----------------------------
    # RUN BACKEND ENGINE
    # -----------------------------
    result = run_engine("REL_STREAMLIT_UPLOAD")

    # -----------------------------
    # RUN LLM
    # -----------------------------
    llm = OllamaLLM(model="mistral")
    ai_engine = ReleaseRiskAIEngine(llm)
    ai_output = ai_engine.generate(result)

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------
    st.subheader("Release Risk Result")

    st.metric("Risk Score", result["risk_score"])
    st.write(f"### Risk Level: {result['risk_level']}")

    st.subheader("AI Explanation")
    st.write(ai_output)
