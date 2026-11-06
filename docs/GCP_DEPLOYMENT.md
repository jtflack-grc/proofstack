# Google Cloud deployment

ProofStack intentionally uses a small cloud footprint:

- **Cloud Run** — reviewer application
- **Firestore** — reviewer decision log
- **Vertex AI / Gemini** — optional live-model fallback if NVIDIA event access is unavailable
- **Secret Manager** — NVIDIA API key only when the NVIDIA provider is enabled

Cloud Storage remains optional. Do not add it merely to increase the service count.

## Security model

Use a dedicated, user-managed Cloud Run service account. Do not download a service-account JSON key and do not set `GOOGLE_APPLICATION_CREDENTIALS` on Cloud Run.

The application uses Google Cloud Application Default Credentials through the attached Cloud Run service identity.

For the current MVP, the runtime identity needs:
- `roles/datastore.user` for Firestore read/write
- `roles/aiplatform.user` only when the Vertex provider is enabled
- `roles/secretmanager.secretAccessor` on the NVIDIA secret only when NVIDIA is enabled

Keep deployer permissions separate from runtime permissions. Do not grant Owner or Editor to the runtime identity.

## 1. Select the project

```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-east1"
gcloud config set project "$GCP_PROJECT_ID"
```

Use the region approved for the BUILD project. Cloud Run/Firestore location and model location do not have to be identical, but each choice should be intentional.

## 2. Enable required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  firestore.googleapis.com \
  iam.googleapis.com \
  secretmanager.googleapis.com \
  aiplatform.googleapis.com
```

Cloud Run source deployment uses Cloud Build and Artifact Registry behind the scenes.

## 3. Create or confirm Firestore

First check whether a database already exists:

```bash
gcloud firestore databases list --project "$GCP_PROJECT_ID"
```

If the project does not already have a suitable default database, create a Firestore Native database only after confirming the location:

```bash
gcloud firestore databases create \
  --database="(default)" \
  --location="$GCP_REGION" \
  --edition=standard \
  --type=firestore-native \
  --project="$GCP_PROJECT_ID"
```

Do not casually recreate or relocate an existing database.

## 4. Create a dedicated runtime identity

```bash
export CLOUD_RUN_SERVICE_ACCOUNT="proofstack-runtime@$GCP_PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create proofstack-runtime \
  --display-name="ProofStack Cloud Run runtime" \
  --project="$GCP_PROJECT_ID"

gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
  --member="serviceAccount:$CLOUD_RUN_SERVICE_ACCOUNT" \
  --role="roles/datastore.user"
```

If Vertex AI is the live provider:

```bash
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
  --member="serviceAccount:$CLOUD_RUN_SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
```

## 5. NVIDIA path

Only configure this after the team has a valid credential.

```bash
export NVIDIA_SECRET_NAME="proofstack-nvidia-api-key"

printf '%s' "$NVIDIA_API_KEY" | gcloud secrets create "$NVIDIA_SECRET_NAME" \
  --data-file=- \
  --replication-policy=automatic \
  --project="$GCP_PROJECT_ID"
```

If the secret already exists, add a version instead.

```bash
gcloud secrets add-iam-policy-binding "$NVIDIA_SECRET_NAME" \
  --member="serviceAccount:$CLOUD_RUN_SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor" \
  --project="$GCP_PROJECT_ID"
```

Then:

```bash
export PROOFSTACK_PROVIDER=nvidia
export NVIDIA_MODEL="confirmed/model-id"
export NVIDIA_SECRET_NAME="proofstack-nvidia-api-key"
bash scripts/deploy_cloud_run.sh
```

## 6. Vertex fallback path

Use this only if the project has Vertex AI access and NVIDIA event access is unavailable.

First run a synthetic smoke test locally or in Cloud Shell with Application Default Credentials:

```bash
export GCP_PROJECT_ID="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
export VERTEX_MODEL="confirmed-model-id"
python scripts/check_vertex.py
```

Then deploy:

```bash
export PROOFSTACK_PROVIDER=vertex
export VERTEX_MODEL="confirmed-model-id"
export GOOGLE_CLOUD_LOCATION="global"
bash scripts/deploy_cloud_run.sh
```

The model ID remains environment-driven. Do not hard-code a model merely because it appears in an example.

## 7. Mock-provider cloud slice

The app can still be deployed with the deterministic mock provider to verify Cloud Run and Firestore independently of model access:

```bash
export PROOFSTACK_PROVIDER=mock
bash scripts/deploy_cloud_run.sh
```

## 8. Public access

The deployment script is private by default. Set:

```bash
export PUBLIC_DEMO=true
```

only when an unauthenticated judging/demo URL is intentionally required.

## 9. Verify

Minimum deployment verification:

1. Cloud Run revision becomes ready.
2. Reviewer page loads.
3. A synthetic evidence case can be assessed.
4. A human decision can be recorded.
5. A new document appears in the configured Firestore collection.
6. Switching evidence clears the prior model assessment.
7. A hallucinated cited excerpt is visibly rejected.
8. Model-overrides require a reviewer note.
9. No secret is visible in the repository, UI, logs, or screenshots.

Do not claim live NVIDIA or Vertex integration until the corresponding smoke test actually succeeds.
