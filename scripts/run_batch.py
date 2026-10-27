import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from proofstack.parser import parse_model_output
from proofstack.providers import get_provider

questions = {q["question_id"]: q for q in json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8"))}
with (ROOT / "data/evidence_manifest.csv").open(encoding="utf-8", newline="") as f:
    evidence = list(csv.DictReader(f))

rows = []
provider = get_provider()
for item in evidence:
    text = (ROOT / item["path"]).read_text(encoding="utf-8")
    parsed = parse_model_output(provider.assess(questions[item["question_id"]], item, text))
    rows.append({
        "question_id": item["question_id"],
        "evidence_id": item["evidence_id"],
        "predicted_label": parsed.label,
        "parse_status": parsed.parse_status,
        "rationale": parsed.rationale,
        "cited_excerpt": parsed.cited_excerpt,
    })

out = ROOT / "results/predictions.csv"
out.parent.mkdir(exist_ok=True)
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)
print(out)
