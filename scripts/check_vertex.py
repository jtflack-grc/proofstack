"""Run one synthetic ProofStack assessment through Google Vertex AI.

Uses Application Default Credentials.

Usage:
    export GCP_PROJECT_ID=...
    export GOOGLE_CLOUD_LOCATION=global
    export VERTEX_MODEL=<confirmed-model-id>
    python scripts/check_vertex.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from proofstack.parser import parse_model_output
from proofstack.providers.google_vertex import GoogleVertexProvider


def main():
    provider = GoogleVertexProvider()

    question = {
        "question_id": "SMOKE-Q1",
        "question": "Is privileged access protected by MFA?",
        "claim": "All privileged accounts use MFA.",
    }
    evidence = {
        "evidence_id": "SMOKE-E1",
        "title": "Synthetic MFA configuration export",
        "artifact_type": "system_export",
    }
    evidence_text = (
        "Synthetic test data only. Privileged accounts in scope: 4. "
        "MFA enrolled: 4. MFA not enrolled: 0."
    )

    raw = provider.assess(question, evidence, evidence_text)
    parsed = parse_model_output(raw)

    print(f"Project: {provider.project}")
    print(f"Location: {provider.location}")
    print(f"Model: {provider.model}")
    print(f"Label: {parsed.label}")
    print(f"Parse status: {parsed.parse_status}")
    print(f"Rationale: {parsed.rationale}")
    print(f"Cited excerpt: {parsed.cited_excerpt}")

    if parsed.label == "UNPARSEABLE":
        raise SystemExit("Vertex request succeeded but model output was not parseable")


if __name__ == "__main__":
    main()
