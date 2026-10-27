import os
from google.cloud import firestore

def append_decision(row: dict):
    project = os.getenv("GCP_PROJECT_ID") or None
    collection = os.getenv("FIRESTORE_COLLECTION", "proofstack_decisions")
    client = firestore.Client(project=project)
    client.collection(collection).add(row)
