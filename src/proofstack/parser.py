import json
import re
from proofstack import LABELS, UNPARSEABLE
from proofstack.schema import ModelAssessment

def _valid(label):
    value = str(label or "").strip().upper()
    return value if value in LABELS else None

def parse_model_output(text: str) -> ModelAssessment:
    raw = str(text or "").strip()
    if not raw:
        return ModelAssessment(label=UNPARSEABLE, parse_status="empty", raw=raw)

    candidates = [raw]
    match = re.search(r"\{.*?\}", raw, flags=re.S)
    if match and match.group(0) != raw:
        candidates.append(match.group(0))

    for candidate in candidates:
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        label = _valid(obj.get("label"))
        if label:
            return ModelAssessment(
                label=label,
                rationale=str(obj.get("rationale", "")).strip(),
                cited_excerpt=str(obj.get("cited_excerpt", "")).strip(),
                parse_status="json",
                raw=raw,
            )

    labels = {m.upper() for m in re.findall(r"\b(SUPPORTED|UNSUPPORTED)\b", raw, flags=re.I)}
    if len(labels) == 1:
        return ModelAssessment(label=next(iter(labels)), rationale=raw[:500], parse_status="label_regex", raw=raw)

    return ModelAssessment(label=UNPARSEABLE, rationale=raw[:500], parse_status="unparseable", raw=raw)
