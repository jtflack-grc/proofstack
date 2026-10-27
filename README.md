# ProofStack

**Turn security-questionnaire claims into traceable evidence decisions.**

ProofStack is a four-week Mentor Me Collective BUILD capstone for a reviewer who needs to decide whether an organization's security-questionnaire answer is actually supported by the evidence submitted with it.

The MVP supports **10 security questions** and **20 synthetic evidence documents**. It keeps AI advisory, makes evidence gaps visible, and records a human review decision for every case.

## What it does

1. Select a questionnaire claim.
2. Inspect the evidence submitted for that claim.
3. Ask the configured model for a binary assessment: SUPPORTED or UNSUPPORTED.
4. Show the model rationale and cited excerpt beside the source evidence.
5. Require a human reviewer to record the final decision and notes.
6. Preserve a clean decision log for evaluation and demonstration.

ProofStack does **not** certify compliance, invent missing controls, or replace reviewer judgment.

## BUILD scope

- 10 questionnaire questions
- 20 synthetic evidence documents
- manually labeled supported/unsupported evaluation set
- visible evidence gaps
- reviewer decision log
- meaningful Google Cloud and NVIDIA integration
- reproducible setup and team contribution record

## Proposed architecture

Reviewer UI (Streamlit)
→ questionnaire + evidence pack
→ model provider
  - mock provider for local development
  - NVIDIA NIM-compatible provider for BUILD integration
→ reviewer decision
→ local CSV during development / Firestore for cloud demo

Synthetic evidence may be served from the repo during development and mirrored to Cloud Storage for the deployed demonstration. The app is container-ready for Cloud Run.

## Quick start

1. Create a Python 3.11+ virtual environment.
2. Install requirements: `pip install -r requirements.txt`
3. Validate the seed data: `python scripts/validate_dataset.py`
4. Run tests: `pytest -q`
5. Launch: `streamlit run app.py`

The default provider is `mock`, so no API key is required for local development.

## Configuration

Copy `.env.example` to your local environment or export variables in your shell.

- PROOFSTACK_PROVIDER=mock or nvidia
- NVIDIA_API_BASE=https://integrate.api.nvidia.com/v1
- NVIDIA_API_KEY=
- NVIDIA_MODEL=
- PROOFSTACK_STORAGE=local or firestore
- GCP_PROJECT_ID=
- GCS_BUCKET=
- FIRESTORE_COLLECTION=proofstack_decisions

Never commit API keys, service-account keys, real customer evidence, or personal data.

## Repository map

- `app.py` — reviewer-facing MVP
- `src/proofstack/` — schema, prompting, parsing, evaluation, providers, storage
- `data/questions.json` — 10 questionnaire questions
- `data/evidence/` — 20 synthetic evidence documents
- `data/evidence_manifest.csv` — question-to-document mapping
- `data/gold_labels.csv` — team-owned manual labels; intentionally blank at bootstrap
- `docs/TEAM.md` — proposed ownership lanes to confirm at kickoff
- `docs/KICKOFF.md` — first-meeting agenda
- `docs/PRODUCT_BRIEF.md` — audience, problem, value, success measures
- `docs/ARCHITECTURE.md` — implementation boundaries
- `docs/EVALUATION_PLAN.md` — evaluation protocol
- `docs/SECURITY.md` — threat model and security expectations
- `docs/WEEK1_BACKLOG.md` — starting work, not immutable assignments

## Human authority

The model produces an advisory assessment. The reviewer makes the final decision. Model disagreement is useful evaluation data, not permission to silently override the reviewer.

## Team

ProofStack BUILD team:
- John Flack
- Hans Rony
- Kristan Mack
- Maimuna Chowdhury

Ownership lanes in `docs/TEAM.md` are proposals for kickoff discussion, not permanent assignments.

## Status

Bootstrap ready for team kickoff. See `STATUS.md`.
