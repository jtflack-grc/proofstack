# ProofStack submission package

MMC BUILD requires:
- working code
- README
- 3-page brief
- 8-slide deck
- 5-minute demo

These files are scaffolds only. They must be updated from the final repository state, frozen gold labels, measured model results, deployed architecture, and verified contribution record.

Do not invent metrics, cloud status, NVIDIA participation, hackathon participation, or team contributions.

## Contingency submission story

Assume:
- Vertex AI / Gemini is the live model provider
- Cloud Run hosts the application
- Firestore stores reviewer decisions
- NVIDIA and external hackathons are not part of the final implementation

If reality changes, update the facts. Do not preserve obsolete architecture merely because it appeared in an early plan.

## Finalization order

1. Freeze the 20 manual labels.
2. Verify Vertex access and run the synthetic smoke test.
3. Deploy the Cloud Run / Firestore vertical slice.
4. Run the final evaluation.
5. Review failures and select honest demo cases.
6. Update the brief.
7. Update the deck from the same facts.
8. Record the demo last.

One set of facts should drive all three deliverables.
