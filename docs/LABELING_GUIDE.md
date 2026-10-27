# Manual labeling guide

The 20-document gold set must be labeled by the team. Do not use model output to create the gold labels.

## SUPPORTED
Use SUPPORTED when the submitted evidence directly demonstrates the specific claim for the relevant environment, population or period.

Examples:
- a system export showing privileged accounts and MFA state
- a joined HR/IAM report showing disablement timestamps
- a vulnerability report showing critical findings closed within SLA
- an after-action report showing an exercise occurred

## UNSUPPORTED
Use UNSUPPORTED when the evidence describes intent or a requirement but does not demonstrate the claim, is missing a required part of the claim, concerns the wrong scope/period, or otherwise cannot establish the assertion.

Examples:
- policy says MFA is required but provides no operating evidence
- backup policy exists but no successful restore-test evidence
- IR plan calls for exercises but no completed exercise record exists

## Procedure
1. Read the questionnaire question and claim.
2. Read the entire evidence document.
3. Decide SUPPORTED or UNSUPPORTED without looking at model output.
4. Record reviewer name/initials and a short note.
5. For disagreement, discuss and document the final team judgment.

## Integrity rule
Never change a gold label because the model disagrees. Disagreement is an evaluation result.
