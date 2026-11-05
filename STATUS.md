# ProofStack Status

## Ready in repository
- Repository foundation
- 10 questions / 20 synthetic evidence documents
- Gold-label sheet intentionally blank for manual team review
- Local mock provider
- NVIDIA OpenAI-compatible adapter
- NVIDIA model discovery and synthetic smoke-test path
- Reviewer UI skeleton
- stale-assessment case-binding protection
- local CSV decision logging
- Firestore decision logging
- Cloud Run deployment path with user-managed service identity
- CI and unit tests

## Still requires live verification
1. Team manual labels completed and frozen.
2. NVIDIA event credential checked with `scripts/check_nvidia.py`.
3. NVIDIA model selected from models actually visible to that credential.
4. Synthetic NVIDIA smoke assessment succeeds.
5. Google Cloud project/region confirmed.
6. Cloud Run deployment succeeds.
7. Reviewer decision is visibly persisted to Firestore.
8. Team contributions are pushed under individual accounts.
9. Final evaluation is run only after gold labels are frozen.
10. Final brief, deck, and 5-minute demo are completed from measured results.

Nothing in the starter design is sacred, but scope remains deliberately small.
