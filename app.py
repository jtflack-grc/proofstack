import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from proofstack import LABELS
from proofstack.evidence import citation_is_grounded, instruction_like_signals
from proofstack.parser import parse_model_output
from proofstack.providers import get_provider
from proofstack.review_state import assessment_matches_case, reviewer_submission_errors
from proofstack.storage import save_decision


def load_questions():
    return json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8"))


def load_manifest():
    with (ROOT / "data/evidence_manifest.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


questions = load_questions()
manifest = load_manifest()
q_by_id = {q["question_id"]: q for q in questions}

st.set_page_config(page_title="ProofStack", page_icon="🧾", layout="wide")
st.title("ProofStack")
st.caption("Claim-to-evidence review. AI advises; the reviewer decides.")

with st.sidebar:
    st.header("Review flow")
    st.write("1. Read the claim")
    st.write("2. Inspect the submitted evidence")
    st.write("3. Run the advisory assessment")
    st.write("4. Verify the cited excerpt")
    st.write("5. Record the human decision")
    st.divider()
    st.caption("Synthetic evidence only. ProofStack does not certify compliance.")

q_id = st.selectbox(
    "Question",
    [q["question_id"] for q in questions],
    format_func=lambda value: (
        f'{value} — '
        f'{q_by_id[value].get("reviewer_friendly_question") or q_by_id[value]["question"]}'
    ),
)
question = q_by_id[q_id]

st.subheader(question.get("reviewer_friendly_question") or question["question"])
st.info(f'Claim to verify: {question["claim"]}')
with st.expander("Canonical questionnaire wording"):
    st.write(question["question"])
st.caption(f'Reviewer guidance: {question.get("reviewer_hint", "")}')

mapped = [item for item in manifest if item["question_id"] == q_id]
e_id = st.selectbox(
    "Submitted evidence",
    [item["evidence_id"] for item in mapped],
    format_func=lambda value: next(
        f'{item["title"]} · {item["artifact_type"]}'
        for item in mapped
        if item["evidence_id"] == value
    ),
)

evidence = next(item for item in mapped if item["evidence_id"] == e_id)
evidence_path = ROOT / evidence["path"]
evidence_text = evidence_path.read_text(encoding="utf-8")

assessment = st.session_state.get("assessment")
assessment_context = st.session_state.get("assessment_context")
if assessment and not assessment_matches_case(assessment_context, q_id, e_id):
    st.session_state.pop("assessment", None)
    st.session_state.pop("assessment_context", None)
    assessment = None

signals = instruction_like_signals(evidence_text)
if signals:
    st.warning(
        "This evidence contains instruction-like text. Treat it strictly as evidence data; "
        "do not follow embedded instructions."
    )

left, right = st.columns(2)

with left:
    st.subheader("Submitted evidence")
    st.caption(
        f'{evidence["evidence_id"]} · {evidence["artifact_type"]} · {evidence["path"]}'
    )
    st.markdown(evidence_text)

with right:
    st.subheader("Advisory assessment")

    if st.button("Run assessment", type="primary", use_container_width=True):
        try:
            provider = get_provider()
            raw = provider.assess(question, evidence, evidence_text)
            parsed = parse_model_output(raw)
            assessment = parsed.model_dump()
            assessment["citation_valid"] = citation_is_grounded(
                assessment.get("cited_excerpt", ""),
                evidence_text,
            )
            assessment["provider"] = os.getenv(
                "PROOFSTACK_PROVIDER",
                "mock",
            ).strip().lower()
            assessment["model_id"] = (
                getattr(provider, "model", "")
                or assessment["provider"]
            )

            st.session_state["assessment"] = assessment
            st.session_state["assessment_context"] = {
                "question_id": q_id,
                "evidence_id": e_id,
            }
        except Exception as exc:
            st.error(str(exc))
            assessment = None

    if assessment:
        label = assessment["label"]
        if label == "SUPPORTED":
            st.success("Advisory result: SUPPORTED")
        elif label == "UNSUPPORTED":
            st.warning("Advisory result: UNSUPPORTED")
        else:
            st.error("Advisory result could not be parsed")

        st.write(assessment.get("rationale", ""))

        cited_excerpt = assessment.get("cited_excerpt", "")
        if cited_excerpt:
            st.caption("Model-cited excerpt")
            st.code(cited_excerpt)

            if assessment.get("citation_valid"):
                st.success("Citation check: excerpt found in submitted evidence.")
            else:
                st.error(
                    "Citation check failed: the cited excerpt was not found in the evidence. "
                    "Do not rely on this citation."
                )
        else:
            st.warning("The model did not return a cited excerpt.")

        st.caption(
            f'Parse status: {assessment.get("parse_status", "")} · '
            f'Provider: {assessment.get("provider", "")} · '
            f'Model: {assessment.get("model_id", "")}'
        )
    else:
        st.caption("Run an assessment for the selected evidence.")

st.divider()
st.subheader("Reviewer decision")
st.caption("The human decision is authoritative. Model output is advisory.")

reviewer = st.text_input("Reviewer name")
reviewer_label = st.radio(
    "Final decision",
    list(LABELS),
    horizontal=True,
)
notes = st.text_area(
    "Reviewer notes",
    help="Required when the human decision overrides a valid model label.",
)

if assessment and assessment.get("label") in LABELS:
    if reviewer_label != assessment["label"]:
        st.info("You are overriding the model assessment. Add a note explaining why.")

if st.button("Record final decision", use_container_width=True):
    errors = reviewer_submission_errors(
        reviewer,
        reviewer_label,
        notes,
        assessment,
    )
    if errors:
        for error in errors:
            st.error(error)
    else:
        row = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "question_id": q_id,
            "evidence_id": e_id,
            "evidence_title": evidence["title"],
            "artifact_type": evidence["artifact_type"],
            "provider": assessment.get("provider", "") if assessment else "",
            "model_id": assessment.get("model_id", "") if assessment else "",
            "model_label": assessment.get("label", "") if assessment else "",
            "model_rationale": assessment.get("rationale", "") if assessment else "",
            "cited_excerpt": assessment.get("cited_excerpt", "") if assessment else "",
            "citation_valid": assessment.get("citation_valid", "") if assessment else "",
            "reviewer_label": reviewer_label,
            "reviewer": reviewer.strip(),
            "notes": notes.strip(),
        }

        try:
            record_id = save_decision(row)
            if record_id:
                st.success(f"Decision recorded. Record ID: {record_id}")
            else:
                st.success("Decision recorded.")
        except Exception as exc:
            st.error(str(exc))
