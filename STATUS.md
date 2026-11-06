# ProofStack Status — contingency path

## Delivery assumption

The contingency build assumes:
- no NVIDIA event credential becomes available
- no external hackathon work is required for completion
- Google Cloud is the primary platform path
- Vertex AI / Gemini is the live model provider
- deterministic mock mode remains available for local/offline demonstration

NVIDIA is optional and must not block the capstone.

## Live cloud verification completed — November 6, 2026

- Google Cloud project: `proofstack-build`
- Vertex model: `gemini-3.8-flash`
- Vertex structured assessment smoke test: PASS
- citation grounding in live smoke test: PASS
- Firestore synthetic write/read/delete smoke test: PASS
- Cloud Run service `proofstack` deployed privately in `us-east1`
- deployed revision `proofstack-00001-j2w` served 100% of traffic
- Cloud Run returned HTTP 200 through the authenticated proxy
- Streamlit UI was exercised locally in Cloud Shell against live Vertex + Firestore
- a reviewer decision was successfully persisted

The currently deployed Cloud Run revision predates the latest UX/security-hardening commits on the contingency branch. Redeploy once before the final demo; this is an application revision update, not additional cloud architecture work.

## Ready in repository

- 10 questions / 20 synthetic evidence documents
- reviewer-friendly language plus canonical claims
- plain-language reviewer workflow
- inert rendering for untrusted evidence and model rationale
- gold-label sheet intentionally blank for manual review
- deterministic mock provider
- Vertex AI / Gemini provider using Application Default Credentials
- optional NVIDIA provider retained but not required
- structured Vertex output schema
- citation grounding checks
- expanded instruction-like evidence detection
- fail-closed model-output parsing
- 20,000-character evidence input boundary
- bounded model output tokens
- stale-assessment case binding
- reviewer identity and override-note validation
- local CSV decision logging
- Firestore decision logging
- Cloud Run deployment path with user-managed service identity
- evaluation provenance including citation-valid status
- OWASP/NIST-aligned security test matrix
- live synthetic adversarial provider probe script
- dependency update automation
- UI rendering-boundary regression tests
- final brief / deck / demo scaffolds
- CI

## Final evaluation completed — November 6, 2026

- gold set completed and frozen: 20/20
- gold distribution: 9 SUPPORTED / 11 UNSUPPORTED
- live security probes: 4/4 passed
- final Vertex evaluation: 19/20 correct (95% accuracy)
- macro F1: 94.99%
- parse success: 100%
- citation grounding: 100%
- single error: Q06 / E12 false support caused by missed current-quarter scope
- detailed results: `docs/EVALUATION_RESULTS.md`

## Remaining delivery work

1. Update the brief, deck, demo script, and results checklist from the verified results.
2. Redeploy the final branch revision before the demo.
3. Reconcile the final team contribution record with work actually delivered.

## Optional only

- NVIDIA event/API access
- NVIDIA smoke test
- external hackathon participation

None of these should delay the contingency submission unless MMC explicitly changes the BUILD requirements.
