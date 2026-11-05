# Google Cloud deployment

ProofStack intentionally uses a small cloud footprint:

- **Cloud Run** — reviewer application
- **Firestore** — reviewer decision log
- **Secret Manager** — NVIDIA API key only when the NVIDIA provider is enabled

Cloud Storage remains optional. Do not add it merely to increase the service count.

## Security model

Use a dedicated, user-managed Cloud Run service account. Do not download a service-account JSON key and do not set `GOOGLE_APPLICATION_CREDENTIALS` on Cloud Run.

The application uses Google Cloud Application Default Credentials through the attached Cloud Run service identity.

For the current MVP, the runtime identity needs:
- `roles/datastore.user` for Firestore read/write
- `roles/secretmanager.secretAccessor` on the NVIDIA secret only, if NVIDIA is enabled

Keep deployer permissions separate from runtime permissions.

## 1. Select the project

```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-east1"
gcloud config set project "$GCP_PROJECT_ID"
```

Use the region approved for the BUILD project. Keep Cloud Run and Firestore geographically sensible for the demo.

## 2. Enable required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  firestore.googleapis.com \
  iam.googleapis.com \
  secretmanager.googleapis.com
```

Cloud Run source deployment uses Cloud Build and Artifact Registry behind the scenes.

## 3. Create or confirm Firestore

First check whether a database already exists:

```bash
gcloud firestore databases list --project "$GCP_PROJECT_ID"
```

If the project does not already have a suitable default database, create a Firestore Native database only after the team confirms the location:

```bash
gcloud firestore databases create \
  --database="(default)" \
  --location="$GCP_REGION" \
  --edition=standard \
  --type=firestore-native \
  --project="$GCP_PROJECT_ID"
```

**Do not casually recreate or relocate an existing database.** Firestore location is an architectural decision and may already be constrained by the project.

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

Do not grant Owner or Editor to the runtime identity.

## 5. Optional: store the NVIDIA key in Secret Manager

Only do this after the team has a valid event/API credential.

```bash
export NVIDIA_SECRET_NAME="proofstack-nvidia-api-key"

printf '%s' "$NVIDIA_API_KEY" | gcloud secrets create "$NVIDIA_SECRET_NAME" \
  --data-file=- \
  --replication-policy=automatic \
  --project="$GCP_PROJECT_ID"
```

If the secret already exists, add a new version rather than creating it again:

```bash
printf '%s' "$NVIDIA_API_KEY" | gcloud secrets versions add "$NVIDIA_SECRET_NAME" \
  --data-file=- \
  --project="$GCP_PROJECT_ID"
```

Grant the runtime identity access to only that secret:

```bash
gcloud secrets add-iam-policy-binding "$NVIDIA_SECRET_NAME" \
  --member="serviceAccount:$CLOUD_RUN_SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor" \
  --project="$GCP_PROJECT_ID"
```

## 6. Deploy

For the mock-provider cloud slice:

```bash
export PROOFSTACK_PROVIDER=mock
export PUBLIC_DEMO=false
bash scripts/deploy_cloud_run.sh
```

For NVIDIA after the credential/model smoke test succeeds:

```bash
export PROOFSTACK_PROVIDER=nvidia
export NVIDIA_MODEL="confirmed/model-id"
export NVIDIA_SECRET_NAME="proofstack-nvidia-api-key"
export PUBLIC_DEMO=false
bash scripts/deploy_cloud_run.sh
```

Set `PUBLIC_DEMO=true` only when the team intentionally wants an unauthenticated judging/demo URL.

## 7. Verify

Minimum deployment verification:

1. Cloud Run revision becomes ready.
2. Reviewer page loads.
3. A synthetic evidence case can be assessed.
4. A human decision can be recorded.
5. A new document appears in the configured Firestore collection.
6. Switching evidence does not retain the previous case's model assessment.
7. No secret is visible in the repository, application UI, logs, or screenshots.

## Definition of done for Issue #6

Do not close the deployment issue simply because a script exists. Close it after a teammate can reproduce the deployment and a reviewer decision is visibly persisted in Firestore.
