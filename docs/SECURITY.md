# Security and threat model

## Data boundary

All committed evidence is synthetic. Do not upload or commit real organizational evidence, credentials, customer data, employee data or confidential questionnaire responses.

## Trust boundaries

### Evidence is untrusted input

Evidence may contain text that resembles instructions to the model. It remains data. It cannot change application permissions, select providers, write records, call tools, or authorize a decision.

### Model output is untrusted advisory output

A valid model label does not make the underlying rationale or citation trustworthy. ProofStack independently checks whether the returned cited excerpt appears in the submitted evidence.

### Human decision is authoritative

The reviewer makes the final SUPPORTED/UNSUPPORTED decision. When the reviewer overrides a valid model label, ProofStack requires a note to preserve the reason for disagreement.

## Primary threats and controls

### Secret exposure

Risk: API keys or service-account material enter Git history.

Controls:
- environment variables or platform secret stores
- Cloud Run Application Default Credentials
- no downloaded service-account keys
- repository review before demo
- no secrets in screenshots

### Prompt injection in evidence

Risk: evidence contains text such as "ignore previous instructions" or tries to force a label.

Controls:
- evidence is explicitly marked as untrusted in the system/model prompt
- model has no external tools or approval authority
- reviewer sees the source evidence
- UI warns when common instruction-like phrases are detected
- mock-provider regression test verifies evidence instructions do not control the label

### Hallucinated citation

Risk: model returns an excerpt not found in the evidence.

Controls:
- exact/whitespace-normalized citation grounding check
- failed citations are visibly marked invalid
- reviewer can still make the final decision
- error is retained in the decision/evaluation record

### Unsupported model confidence

Risk: model asserts support not present in evidence.

Controls:
- binary output parser fails closed to UNPARSEABLE
- ambiguous output is never silently converted into a valid label
- human final decision
- final evaluation against a manually frozen gold set

### Evidence/claim mismatch

Risk: document is mapped to the wrong question.

Controls:
- explicit manifest
- question/evidence IDs shown in UI and logs
- validation script checks 10 questions, 20 unique evidence IDs and paths, and exactly two documents per question

### Stale assessment crossing cases

Risk: assessment for one evidence item is accidentally written against another.

Controls:
- assessment state is bound to question_id + evidence_id
- switching cases clears stale model state
- unit tests cover question/evidence mismatch

### Decision-log integrity

Risk: final decisions cannot be traced or reviewer overrides are unexplained.

Controls:
- append-style local logging
- Firestore server timestamps in cloud mode
- reviewer identity required
- override note required
- provider/model, rationale, cited excerpt and citation-valid flag retained

### Excess permissions

Risk: cloud runtime identity has unnecessary access.

Controls:
- dedicated user-managed Cloud Run service identity
- Firestore access uses roles/datastore.user
- Vertex path uses roles/aiplatform.user only when required
- NVIDIA secret access is granted only to the specific secret
- no Owner/Editor runtime grant

## Abuse/regression cases

Automated tests cover:
- evidence says "ignore previous instructions"
- embedded and malformed model output
- ambiguous SUPPORTED/UNSUPPORTED text
- hallucinated citation
- stale assessment context
- reviewer missing identity
- human override without explanation
- missing NVIDIA key/model configuration
- NVIDIA HTTP/malformed-response failure
- Firestore collection/config behavior
- Vertex missing project/model configuration and response handling

## Deployment review

Before public demo:
- verify no secrets in repo/history
- confirm IAM
- verify synthetic-only dataset
- run CI
- run the selected live-provider smoke test
- verify Firestore persistence
- rehearse one weak-evidence and one strong-evidence case
- document known limitations
