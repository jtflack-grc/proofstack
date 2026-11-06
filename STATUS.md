# ProofStack Status — contingency path

## Delivery assumption

The contingency build assumes:
- no NVIDIA event credential becomes available
- no external hackathon work is required for completion
- Google Cloud is the primary platform path
- Vertex AI / Gemini is the intended live model provider
- deterministic mock mode remains available for local/offline demonstration

NVIDIA is optional and must not block the capstone.

## Ready in repository

- 10 questions / 20 synthetic evidence documents
- reviewer-friendly language plus canonical claims
- gold-label sheet intentionally blank for manual review
- deterministic mock provider
- Vertex AI / Gemini provider using Application Default Credentials
- optional NVIDIA provider retained but not required
- citation grounding checks
- instruction-like evidence warnings
- fail-closed model-output parsing
- stale-assessment case binding
- reviewer identity and override-note validation
- local CSV decision logging
- Firestore decision logging
- Cloud Run deployment path with user-managed service identity
- evaluation provenance and error-analysis tooling
- security regression tests
- final brief / deck / demo scaffolds
- CI

## Still requires live verification

1. Manual labels are completed and frozen.
2. Google Cloud project and approved locations are confirmed.
3. A Vertex model available to that project is selected.
4. `python scripts/check_vertex.py` succeeds on synthetic data.
5. Cloud Run deployment succeeds.
6. Reviewer decision is visibly persisted to Firestore.
7. Final model evaluation runs only after gold labels are frozen.
8. Error-analysis cases are reviewed.
9. Brief, deck and demo are updated from the same verified facts.
10. Final team contribution record reflects actual work completed.

## Optional only

- NVIDIA event/API access
- NVIDIA smoke test
- external hackathon participation

None of these should delay the contingency submission unless MMC explicitly changes the BUILD requirements.
