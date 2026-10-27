import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
questions = json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8"))
with (ROOT / "data/evidence_manifest.csv").open(encoding="utf-8", newline="") as f:
    evidence = list(csv.DictReader(f))

assert len(questions) == 10, f"Expected 10 questions, found {len(questions)}"
assert len(evidence) == 20, f"Expected 20 evidence docs, found {len(evidence)}"
qids = {q["question_id"] for q in questions}
assert len(qids) == 10
counts = Counter(e["question_id"] for e in evidence)
assert set(counts) == qids
assert all(v == 2 for v in counts.values()), counts
assert len({e["evidence_id"] for e in evidence}) == 20
for e in evidence:
    assert (ROOT / e["path"]).exists(), e["path"]
print("OK: 10 questions, 20 evidence documents, 2 documents per question")
