# ProofStack

**Turn security-questionnaire claims into traceable evidence decisions.**

ProofStack is a human-in-the-loop MMC BUILD capstone for a reviewer who needs to decide whether a security-questionnaire claim is actually supported by the evidence submitted with it.

The MVP contains **10 security questions** and **20 synthetic evidence documents**. AI is advisory. The reviewer remains the final authority.

## Final result

The frozen 20-case evaluation used Vertex AI with `gemini-3.8-flash`.

- **Accuracy:** 95.0% (19/20)
- **Macro precision:** 95.0%
- **Macro recall:** 95.45%
- **Macro F1:** 94.99%
- **Parse success:** 100% (20/20)
- **Citation grounding:** 100% (20/20)
- **Live adversarial probes:** 4/4 passed
- **Gold set:** 9 SUPPORTED / 11 UNSUPPORTED

The single model error was Q06 / E12: strong backup/restore evidence from Q3 was incorrectly accepted for a claim requiring evidence from the **current quarter**. The citation was real and the judgment was still wrong.

> **Grounded does not mean correct.**

That is the central reason ProofStack preserves human judgment.

## What it does

1. Select a questionnaire claim.
2. Inspect the evidence submitted for that claim.
3. Ask the configured model for a binary advisory assessment: SUPPORTED or UNSUPPORTED.
4. Show the model rationale and cited excerpt beside the source evidence.
5. Independently verify that the cited excerpt is present in the evidence.
6. Require a human reviewer to record the final decision.
7. Preserve a traceable decision record for evaluation and review.

ProofStack does **not** certify compliance, invent missing controls, or replace reviewer judgment.

## Reviewer flow

`question → claim → evidence → AI advisory → citation check → human decision → traceable record`

The evidence set intentionally pairs weaker policy/procedure artifacts with stronger operational/configuration artifacts so the reviewer can distinguish control intent from demonstrated operation.

## Live architecture

```text
Streamlit reviewer UI on Cloud Run
        ↓
Vertex AI / Gemini 3.8 Flash
        ↓
strict parser + exact citation grounding
        ↓
human reviewer decision
        ↓
Firestore decision record
```

The Cloud Run service is private by default and uses a dedicated runtime service identity rather than a downloaded service-account key.

## Security posture

ProofStack treats both evidence and model output as untrusted boundaries.

Implemented controls include:

- evidence explicitly marked as untrusted model input
- dynamic evidence kept out of the static system instruction
- 20,000-character evidence input limit
- bounded model output and request timeout/retry behavior
- structured Vertex response schema
- fail-closed parsing for ambiguous output
- exact/whitespace-normalized citation grounding
- evidence and model rationale rendered as inert text
- stale assessment state cleared when the case changes
- reviewer identity required
- reviewer explanation required when overriding a valid model label
- model has no tools or approval authority
- private Cloud Run deployment by default
- dedicated runtime service identity
- OWASP Top 10:2025 / OWASP GenAI LLM Top 10 2026 / NIST AI RMF mapping

Four live synthetic adversarial probes passed against the final Vertex model: direct label override, fake system prompt, role hijack, and Markdown-like evidence.

See `docs/SECURITY.md` and `docs/SECURITY_TEST_MATRIX.md`.

## Gold-set integrity

The primary reviewer completed all 20 labels before the final model predictions were generated. Each label includes a short human rationale.

After labeling, the set was frozen with SHA-256:

`1317a4c5cd1b0d02575d2e54d62d8cc03c7508805dd043cf44dc67e2503d6b74`

The evaluation script verifies the frozen hash before scoring and refuses to evaluate a modified gold set without a deliberate re-freeze.

See `results/gold_set_manifest.json`.

## Evaluation artifacts

- `results/predictions.csv` — all 20 final model predictions
- `results/run_metadata.json` — provider/model/commit provenance
- `results/metrics.json` — final classification, parse and citation metrics
- `results/error_analysis.csv` — disagreement/citation-failure review
- `results/security_probes.csv` — live adversarial probe results
- `results/final_summary.md` — human-readable evaluation summary
- `docs/EVALUATION_RESULTS.md` — documented findings and Q06/E12 analysis

The 20-case synthetic evaluation is descriptive. It is not a production benchmark or a generalized compliance-accuracy claim.

## SDG 1 context

The BUILD connection to **SDG 1: No Poverty** is intentionally modest. Smaller organizations, nonprofits, and grant applicants can have limited assurance capacity and may face disproportionate evidence-review friction. ProofStack explores whether a transparent review aid can help scarce reviewers focus attention without lowering the assurance standard. The project does not claim direct poverty reduction.

## Quick start

1. Create a Python 3.11+ virtual environment.
2. Install requirements: `pip install -r requirements.txt`
3. Validate the seed data: `python scripts/validate_dataset.py`
4. Run tests: `pytest -q`
5. Launch locally: `streamlit run app.py`

The default provider is `mock`, so local development does not require cloud credentials.

## Vertex configuration

Primary live settings:

- `PROOFSTACK_PROVIDER=vertex`
- `GOOGLE_CLOUD_PROJECT=proofstack-build`
- `GOOGLE_CLOUD_LOCATION=global`
- `VERTEX_MODEL=gemini-3.8-flash`
- `VERTEX_MAX_TOKENS=800`
- `VERTEX_THINKING_LEVEL=LOW`
- `VERTEX_TIMEOUT_MS=45000`
- `VERTEX_RETRY_ATTEMPTS=2`
- `PROOFSTACK_MAX_EVIDENCE_CHARS=20000`
- `PROOFSTACK_STORAGE=firestore`
- `GCP_REGION=us-east1`
- `FIRESTORE_COLLECTION=proofstack_decisions`

Never commit API keys, service-account keys, real customer evidence, or personal data.

## Repository map

- `app.py` — reviewer-facing MVP
- `src/proofstack/` — schema, prompting, parsing, evaluation, providers, storage
- `data/questions.json` — 10 questionnaire questions
- `data/evidence/` — 20 synthetic evidence documents
- `data/evidence_manifest.csv` — question-to-document mapping
- `data/gold_labels.csv` — completed human reference labels
- `docs/SECURITY.md` — threat model and security controls
- `docs/SECURITY_TEST_MATRIX.md` — OWASP/NIST mapping and acceptance cases
- `docs/EVALUATION_PLAN.md` — evaluation protocol
- `docs/EVALUATION_RESULTS.md` — final results and error analysis
- `docs/GCP_DEPLOYMENT.md` — Cloud Run / Firestore / Vertex deployment
- `deliverables/` — final brief, research paper, deck content, demo script, contribution record and submission gate

## Contribution record

The final contingency implementation was completed by John Flack. Team discussion contributions are recorded separately and are not represented as repository work unless they were actually delivered.

See `deliverables/CONTRIBUTIONS.md`.

## Optional NVIDIA adapter

The repository retains an NVIDIA OpenAI-compatible provider and readiness script. NVIDIA is **not** part of the verified final architecture and did not block the capstone.

## Status

See `STATUS.md`.
