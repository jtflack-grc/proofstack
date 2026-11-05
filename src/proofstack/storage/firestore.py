import os

from google.cloud import firestore


def append_decision(row: dict):
    """Append one reviewer decision using Cloud Run/Application Default Credentials."""
    project = os.getenv("GCP_PROJECT_ID") or None
    collection = os.getenv("FIRESTORE_COLLECTION", "proofstack_decisions").strip()
    if not collection:
        raise RuntimeError("FIRESTORE_COLLECTION must not be empty")

    client = firestore.Client(project=project)
    record = dict(row)
    record["recorded_at_server"] = firestore.SERVER_TIMESTAMP

    _, document_ref = client.collection(collection).add(record)
    return document_ref.id
