# Security and threat model

## Data boundary
All committed evidence is synthetic. Do not upload or commit real organizational evidence, credentials, customer data, employee data or confidential questionnaire responses.

## Primary threats

### Secret exposure
Risk: API keys or service-account material enter Git history.
Controls: environment variables/secret store, gitignore patterns, PR review, no secrets in screenshots.

### Prompt injection in evidence
Risk: an evidence document contains text that tries to instruct the model or application.
Controls: system prompt states evidence is untrusted data; model has no tools/actions; reviewer sees source evidence; output remains advisory.

### Unsupported model confidence
Risk: model asserts support not present in evidence.
Controls: require cited excerpt, strict binary parser, human final decision, evaluation against manual labels.

### Evidence/claim mismatch
Risk: document is mapped to the wrong question.
Controls: explicit manifest, IDs shown in UI/logs, validation script checks mappings.

### Decision-log integrity
Risk: final decisions cannot be traced or are overwritten.
Controls: append-style local logging for development; Firestore record IDs/timestamps for cloud demo; reviewer identity field.

### Excess permissions
Risk: cloud identity has unnecessary access.
Controls: least privilege, separate runtime identity, only required Storage/Firestore permissions.

## Abuse cases to test
- evidence says "ignore prior instructions"
- model returns prose without a valid label
- model cites text not present in evidence
- missing API key
- missing evidence file
- invalid question/evidence mapping
- reviewer submits without a final decision

## Deployment review
Before public demo: verify no secrets in repo/history, confirm IAM, verify synthetic-only dataset, test error handling, and document known limitations.
