# Final-results gate

## Dataset
- [x] 20/20 manual labels complete
- [x] gold labels frozen before final model run
- [x] reviewer name and rationale recorded
- [x] gold SHA-256 manifest created
- [x] gold distribution recorded: 9 SUPPORTED / 11 UNSUPPORTED

## Vertex AI
- [x] GCP project confirmed: `proofstack-build`
- [x] final model confirmed: `gemini-3.8-flash`
- [x] structured Vertex smoke test passed
- [x] final 20-case model run completed

## Google Cloud
- [x] Cloud Run deployment verified
- [x] Firestore persistence verified
- [x] private access choice intentional
- [x] no downloaded service-account key used
- [x] synthetic-only evidence used
- [ ] redeploy the final hardened branch revision before the recorded/live demo

## Security
- [x] prompt-injection boundary implemented
- [x] inert evidence/model rendering implemented
- [x] structured output schema implemented
- [x] citation grounding implemented
- [x] oversized evidence fails closed
- [x] bounded Vertex timeout/retry behavior implemented
- [x] 4/4 live adversarial probes passed
- [x] OWASP / NIST security mapping documented

## Evaluation
- [x] predictions generated for all 20 cases
- [x] accuracy calculated: 95.0%
- [x] macro precision calculated: 95.0%
- [x] macro recall calculated: 95.45%
- [x] macro F1 calculated: 94.99%
- [x] parse success calculated: 100%
- [x] citation grounding calculated: 100%
- [x] confusion matrix reviewed
- [x] false support case inspected: Q06/E12
- [x] no false rejection cases
- [x] limitations documented

## Contribution record
- [x] John contribution recorded
- [x] Hans contribution recorded based on delivered/documented work
- [x] Kristan contribution recorded based on delivered/documented work
- [x] Maimuna contribution recorded based on delivered/documented work

## Submission consistency
- [x] brief uses verified model ID and metrics
- [x] research paper uses verified model ID and metrics
- [x] deck content uses verified model ID and metrics
- [x] demo script uses verified model ID and metrics
- [x] architecture matches deployed services
- [x] limitations are explicit
- [x] no compliance/certification claim
- [x] no production-readiness claim
- [x] no NVIDIA/hackathon claim
