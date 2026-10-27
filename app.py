import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from proofstack.parser import parse_model_output
from proofstack.providers import get_provider
from proofstack.storage import save_decision

def load_questions():
    return json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8"))

def load_manifest():
    with (ROOT / "data/evidence_manifest.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

questions = load_questions()
manifest = load_manifest()
q_by_id = {q["question_id"]: q for q in questions}

st.set_page_config(page_title="ProofStack", layout="wide")
st.title("ProofStack")
st.caption("Claim-to-evidence review. AI advises; the reviewer decides.")

q_id = st.selectbox("Question", [q["question_id"] for q in questions], format_func=lambda x: f'{x} — {q_by_id[x]["question"]}')
question = q_by_id[q_id]
st.info(question["claim"])

mapped = [e for e in manifest if e["question_id"] == q_id]
e_id = st.selectbox("Evidence", [e["evidence_id"] for e in mapped], format_func=lambda x: next(e["title"] for e in mapped if e["evidence_id"] == x))
evidence = next(e for e in mapped if e["evidence_id"] == e_id)
evidence_text = (ROOT / evidence["path"]).read_text(encoding="utf-8")

left, right = st.columns(2)
with left:
    st.subheader("Submitted evidence")
    st.caption(f'{evidence["evidence_id"]} · {evidence["artifact_type"]}')
    st.markdown(evidence_text)
with right:
    st.subheader("Advisory assessment")
    if st.button("Run assessment", type="primary"):
        try:
            raw = get_provider().assess(question, evidence, evidence_text)
            st.session_state["assessment"] = parse_model_output(raw).model_dump()
        except Exception as exc:
            st.error(str(exc))
    assessment = st.session_state.get("assessment")
    if assessment:
        st.metric("Model label", assessment["label"])
        st.write(assessment["rationale"])
        if assessment.get("cited_excerpt"):
            st.code(assessment["cited_excerpt"])
        st.caption(f'Parse status: {assessment["parse_status"]}')

st.divider()
st.subheader("Reviewer decision")
reviewer = st.text_input("Reviewer")
reviewer_label = st.radio("Final decision", ["SUPPORTED", "UNSUPPORTED"], horizontal=True)
notes = st.text_area("Reviewer notes")

if st.button("Record final decision"):
    assessment = st.session_state.get("assessment") or {}
    row = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "question_id": q_id,
        "evidence_id": e_id,
        "model_label": assessment.get("label", ""),
        "reviewer_label": reviewer_label,
        "reviewer": reviewer,
        "notes": notes,
    }
    try:
        save_decision(row)
        st.success("Decision recorded.")
    except Exception as exc:
        st.error(str(exc))

with st.expander("Reviewer hint"):
    st.write(question.get("reviewer_hint", ""))
