import csv
from pathlib import Path

HEADER = ["timestamp_utc","question_id","evidence_id","model_label","reviewer_label","reviewer","notes"]

def append_decision(row: dict, path="local_decisions.csv"):
    target = Path(path)
    new = not target.exists()
    with target.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        if new:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in HEADER})
