# ProofStack — 5-minute demo scaffold

Target: 4:30–4:50 in rehearsal so there is margin.

## 0:00–0:30 — Hook

"Security questionnaires are full of statements like 'we use MFA,' 'we test backups,' or 'we review privileged access.' The difficult part isn't making the claim. It's showing a reviewer evidence that actually proves it.

ProofStack is a small human-in-the-loop workflow for that problem."

## 0:30–1:00 — Show the claim

Open one question.

"This is the exact claim we're reviewing. ProofStack keeps the claim separate from the evidence so the reviewer can see what must actually be proven."

Choose a case that is visually easy to understand.

## 1:00–1:45 — Show weak evidence

Open a policy/procedure artifact.

"This document is relevant, but relevance is not the same as proof. It says what should happen. It does not necessarily show what happened."

Run the model.

Show:
- advisory label
- rationale
- cited excerpt

Do not linger on raw model prose.

## 1:45–2:30 — Show operational evidence

Switch to the paired operational artifact.

The app must clear the previous assessment.

"This is why we bind every model assessment to the exact evidence case. We do not allow one item's assessment to carry into another review."

Run assessment.

Point to the excerpt that grounds the decision.

## 2:30–3:10 — Human decision

"The model does not approve or certify anything. The reviewer records the final decision."

Record reviewer label and a short note.

Show that the decision is persisted.

If using Firestore in the live demo, show only a safe metadata view or screenshot prepared in advance. Do not expose credentials or unnecessary cloud-console clutter.

## 3:10–3:45 — Architecture

Show one simple architecture image/slide.

"ProofStack runs as a small Streamlit application on Cloud Run. The model provider uses NVIDIA's OpenAI-compatible interface. Reviewer decisions are stored in Firestore. The runtime uses a dedicated least-privilege identity."

If a component is not live, state that accurately.

## 3:45–4:30 — Evaluation

Show final measured results.

"Our team manually labeled all 20 evidence items before running the final model evaluation."

State:
- accuracy **[VALUE]**
- macro F1 **[VALUE]**
- parse success **[VALUE]**

Then immediately add:
"This is a tiny synthetic set, so those numbers are descriptive, not a production benchmark."

## 4:30–5:00 — Close

"The useful part of ProofStack isn't that AI can say supported or unsupported. It's that the reviewer can trace the claim to the evidence, see what the model relied on, override it when necessary, and preserve the decision.

The pattern is simple: claim, evidence, analysis, human judgment, traceability."

End on the reviewer UI or final takeaway slide.

## Demo safety net

Before recording:
- use synthetic data only
- have one weak-evidence and one strong-evidence case preselected
- verify NVIDIA credential
- verify Cloud Run URL
- verify Firestore write
- close unrelated browser tabs
- hide bookmarks/account notifications
- have screenshots available if a live cloud console step fails
- never expose API key or secret values
