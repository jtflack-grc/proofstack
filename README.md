# ProofStack

**Turn security-questionnaire claims into traceable evidence decisions.**

ProofStack is a four-week Mentor Me Collective BUILD capstone for a reviewer who needs to decide whether an organization's security-questionnaire answer is actually supported by the evidence submitted with it.

The MVP supports **10 security questions** and **20 synthetic evidence documents**. It keeps AI advisory, makes evidence gaps visible, and records a human review decision for every case.

## What it does

1. Select a questionnaire claim.
2. Inspect the evidence submitted for that claim.
3. Ask the configured model for a binary assessment: SUPPORTED or UNSUPPORTED.
4. Show the model rationale and cited excerpt beside the source evidence.
5. Independently check whether the cited excerpt is present in the evidence.
6. Require a human reviewer to record the final decision.
7. Preserve a traceable decision log for evaluation and demonstration.

ProofStack does **not** certify compliance, invent missing controls, or replace reviewer judgment.

## BUILD scope

- 10 questionnaire questions
- 20 synthetic evidence documents
- manually labeled SUPPORTED / UNSUPPORTED evaluation set
- visible evidence gaps
- reviewer decision log
- Google Cloud deployment using Cloud Run and Firestore
- Vertex AI / Gemini live-model path
- reproducible setup and evaluation record

The capstone does not depend on participation in an external hackathon or NVIDIA event. NVIDIA support remains in the repository as an optional provider adapter, but it is not part of the contingency delivery path.

## Architecture

Reviewer UI (Streamlit)
→ questionnaire + synthetic evidence pack
→ model provider
  - mock provider for local/offline development
  - Vertex AI / Gemini for the intended live cloud demonstration
  - optional NVIDIA adapter if credentials independently become available
→ strict output parser + citation grounding check
→ human reviewer decision
→ local CSV during development / Firestore for cloud demonstration

The application is container-ready for Cloud Run and uses a dedicated runtime service identity rather than downloaded service-account keys.

## Quick start

1. Create a Python 3.11+ virtual environment.
2. Install requirements: `pip install -r requirements.txt`
3. Validate the seed data: `python scripts/validate_dataset.py`
4. Run tests: `pytest -q`
5. Launch locally: `streamlit run app.py`

The default provider is `mock`, so local development does not require cloud credentials.

## Vertex AI / Gemini smoke test

The intended live provider for the contingency build is Vertex AI / Gemini using Google Cloud Application Default Credentials.

1. Set `GCP_PROJECT_ID` or `GOOGLE_CLOUD_PROJECT`.
2. Set `GOOGLE_CLOUD_LOCATION` to the approved model location.
3. Set `VERTEX_MODEL` to a model available in the project.
4. Run `python scripts/check_vertex.py`.
5. Set `PROOFSTACK_PROVIDER=vertex`.
6. Deploy with `bash scripts/deploy_cloud_run.sh`.

The smoke test uses synthetic data only.

## Optional NVIDIA adapter

The repository retains an NVIDIA OpenAI-compatible provider and readiness script. It is **not required** for the contingency BUILD path and should not delay submission.

If valid NVIDIA credentials later become available, `python scripts/check_nvidia.py` can list visible models and `python scripts/check_nvidia.py --smoke` can verify one synthetic assessment.

Do not claim NVIDIA integration unless that smoke test actually succeeds.

## Configuration

Copy `.env.example` to your local environment or export variables in your shell.

Primary contingency settings:
- PROOFSTACK_PROVIDER=mock or vertex
- GOOGLE_CLOUD_PROJECT=
- GOOGLE_CLOUD_LOCATION=global
- VERTEX_MODEL=
- VERTEX_MAX_TOKENS=350
- PROOFSTACK_STORAGE=local or firestore
- GCP_PROJECT_ID=
- GCP_REGION=us-east1
- CLOUD_RUN_SERVICE=proofstack
- CLOUD_RUN_SERVICE_ACCOUNT=
- FIRESTORE_COLLECTION=proofstack_decisions

Optional NVIDIA settings remain in `.env.example`.

Never commit API keys, service-account keys, real customer evidence, or personal data.

## Repository map

- `app.py` — reviewer-facing MVP
- `src/proofstack/` — schema, prompting, parsing, evaluation, providers, storage
- `data/questions.json` — 10 questionnaire questions
- `data/evidence/` — 20 synthetic evidence documents
- `data/evidence_manifest.csv` — question-to-document mapping
- `data/gold_labels.csv` — manual labels; intentionally blank until human review
- `docs/CONTINGENCY_BUILD.md` — delivery assumptions and contribution boundaries
- `docs/GCP_DEPLOYMENT.md` — Cloud Run / Firestore / Vertex deployment
- `docs/EVALUATION_PLAN.md` — evaluation protocol
- `docs/SECURITY.md` — threat model and security expectations
- `deliverables/` — brief, deck, demo and final-results scaffolds

## Human authority

The model produces an advisory assessment. The reviewer makes the final decision. Model disagreement is useful evaluation data, not permission to silently override the reviewer.

## Team

ProofStack BUILD team:
- John Flack
- Hans Rony
- Kristan Mack
- Maimuna Chowdhury

The contingency branch is explicitly John-owned implementation insurance. Any teammate contributions that arrive later should retain their real authorship and be reviewed normally.

## Status

See `STATUS.md`.
