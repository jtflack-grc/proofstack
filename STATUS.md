# ProofStack Status — contingency path

## Delivery assumption

The verified final build uses Google Cloud as the primary platform path and Vertex AI / Gemini as the live model provider. NVIDIA remains optional and is not part of the final delivery story.

## Live cloud verification completed — November 6, 2026

- Google Cloud project: `proofstack-build`
- Vertex model: `gemini-3.8-flash`
- Vertex structured assessment smoke test: PASS
- citation grounding in live smoke test: PASS
- Firestore synthetic write/read/delete smoke test: PASS
- Cloud Run service `proofstack` deployed privately in `us-east1`
- deployed revision `proofstack-00001-j2w` served 100% of traffic at the first vertical-slice check
- Cloud Run returned HTTP 200 through the authenticated proxy
- Streamlit UI was exercised against live Vertex + Firestore
- reviewer decision persistence was verified

The currently deployed Cloud Run revision predates the final UX/security/evaluation packaging commits. One final application redeploy is required before the recorded/live demo. No additional cloud architecture work is needed.

## Ready in repository

- 10 questions / 20 synthetic evidence documents
- reviewer-friendly language plus canonical claims
- completed human gold set
- frozen gold SHA-256 manifest
- 9 SUPPORTED / 11 UNSUPPORTED reference labels
- plain-language reviewer workflow
- inert rendering for untrusted evidence and model rationale
- deterministic mock provider
- Vertex AI / Gemini provider using Application Default Credentials
- optional NVIDIA provider retained but not required
- structured Vertex output schema
- citation grounding checks
- expanded instruction-like evidence detection
- fail-closed model-output parsing
- 20,000-character evidence input boundary
- bounded model output tokens
- 45-second Vertex request timeout / 2-attempt bound
- stale-assessment case binding
- reviewer identity and override-note validation
- local CSV decision logging
- Firestore decision logging
- Cloud Run deployment path with user-managed service identity
- evaluation provenance including citation-valid status
- OWASP/NIST-aligned security test matrix
- live synthetic adversarial provider probes
- dependency update automation
- UI rendering-boundary regression tests
- final evaluation artifacts
- final project brief
- final research paper
- final deck content
- final demo script
- final contribution record
- CI

## Final evaluation completed — November 6, 2026

- gold set completed and frozen: 20/20
- gold distribution: 9 SUPPORTED / 11 UNSUPPORTED
- live security probes: 4/4 passed
- final Vertex evaluation: 19/20 correct (95.0% accuracy)
- macro precision: 95.0%
- macro recall: 95.45%
- macro F1: 94.99%
- parse success: 100%
- citation grounding: 100%
- single error: Q06 / E12 false support caused by missed current-quarter scope
- detailed results: `docs/EVALUATION_RESULTS.md`

## Central finding

**Grounded does not mean correct.**

Gemini cited real Q3 backup/restore evidence but incorrectly treated it as sufficient for a claim requiring evidence from the current quarter. The failure was interpretation of temporal scope, not hallucinated evidence or malformed output.

## Final delivery package

- `deliverables/FINAL_BRIEF.md`
- `deliverables/RESEARCH_PAPER.md`
- `deliverables/FINAL_DECK_CONTENT.md`
- `deliverables/FINAL_DEMO_SCRIPT.md`
- `deliverables/CONTRIBUTIONS.md`
- `deliverables/RESULTS_CHECKLIST.md`

## Remaining action

1. Pull the final branch in Cloud Shell.
2. Redeploy the final hardened revision to the existing private Cloud Run service.
3. Perform one short smoke/demo check; do not rerun the final 20-case evaluation.
4. Submit/present the packaged artifacts using the exact MMC portal fields when they are available.

## Optional only

- NVIDIA event/API access
- NVIDIA smoke test
- external hackathon participation
- larger dataset or additional model experiments

None of these are required to complete the current contingency delivery.
