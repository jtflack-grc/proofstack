#!/usr/bin/env bash
set -euo pipefail

: "${GCP_PROJECT_ID:?Set GCP_PROJECT_ID}"
: "${CLOUD_RUN_SERVICE_ACCOUNT:?Set CLOUD_RUN_SERVICE_ACCOUNT to a user-managed service account}"

GCP_REGION="${GCP_REGION:-us-east1}"
CLOUD_RUN_SERVICE="${CLOUD_RUN_SERVICE:-proofstack}"
FIRESTORE_COLLECTION="${FIRESTORE_COLLECTION:-proofstack_decisions}"
PROOFSTACK_PROVIDER="${PROOFSTACK_PROVIDER:-mock}"
PUBLIC_DEMO="${PUBLIC_DEMO:-false}"

args=(
  gcloud run deploy "${CLOUD_RUN_SERVICE}"
  --source .
  --project "${GCP_PROJECT_ID}"
  --region "${GCP_REGION}"
  --service-account "${CLOUD_RUN_SERVICE_ACCOUNT}"
  --set-env-vars "PROOFSTACK_STORAGE=firestore,GCP_PROJECT_ID=${GCP_PROJECT_ID},FIRESTORE_COLLECTION=${FIRESTORE_COLLECTION},PROOFSTACK_PROVIDER=${PROOFSTACK_PROVIDER}"
)

if [[ "${PROOFSTACK_PROVIDER}" == "nvidia" ]]; then
  : "${NVIDIA_MODEL:?Set NVIDIA_MODEL when PROOFSTACK_PROVIDER=nvidia}"
  : "${NVIDIA_SECRET_NAME:?Set NVIDIA_SECRET_NAME to an existing Secret Manager secret}"

  args+=(
    --update-env-vars "NVIDIA_MODEL=${NVIDIA_MODEL},NVIDIA_API_BASE=${NVIDIA_API_BASE:-https://integrate.api.nvidia.com/v1}"
    --update-secrets "NVIDIA_API_KEY=${NVIDIA_SECRET_NAME}:latest"
  )
fi

if [[ "${PUBLIC_DEMO}" == "true" ]]; then
  args+=(--allow-unauthenticated)
else
  args+=(--no-allow-unauthenticated)
fi

echo "Deploying ${CLOUD_RUN_SERVICE} to ${GCP_PROJECT_ID}/${GCP_REGION}"
echo "Runtime identity: ${CLOUD_RUN_SERVICE_ACCOUNT}"
echo "Provider: ${PROOFSTACK_PROVIDER}"
echo "Public demo: ${PUBLIC_DEMO}"

"${args[@]}"
