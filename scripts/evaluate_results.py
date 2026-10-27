import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from proofstack.evaluation import classification_metrics

def read(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

gold = read(ROOT / "data/gold_labels.csv")
pred = read(ROOT / "results/predictions.csv")
gold_by = {r["evidence_id"]: r["label"] for r in gold if r["label"]}
pred_by = {r["evidence_id"]: r["predicted_label"] for r in pred}
missing = [k for k,v in gold_by.items() if k not in pred_by]
if missing:
    raise SystemExit(f"Missing predictions: {missing}")
if len(gold_by) != 20:
    raise SystemExit("Gold labels are incomplete; manually label all 20 documents first.")
labels = list(gold_by)
metrics = classification_metrics([gold_by[k] for k in labels], [pred_by[k] for k in labels])
parse_success = sum(pred_by[k] in ("SUPPORTED","UNSUPPORTED") for k in labels) / len(labels)
metrics["parse_success_rate"] = parse_success
out = ROOT / "results/metrics.json"
out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
print(json.dumps(metrics, indent=2))
