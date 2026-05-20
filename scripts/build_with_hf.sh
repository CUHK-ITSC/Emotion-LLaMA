#!/bin/sh
set -e
if [ -z "$HF_TOKEN" ]; then
  echo "HF_TOKEN environment variable is required for build-time download (export HF_TOKEN=...)"
  exit 1
fi

TMPFILE="hf_token.txt"
echo "Writing token to $TMPFILE (will be removed after build)"
printf "%s" "$HF_TOKEN" > "$TMPFILE"

echo "Building image with BuildKit; this will pass the token as a build secret."
DOCKER_BUILDKIT=1 docker build --secret id=hf_token,src="$TMPFILE" -t emotion-llama:latest .

rm -f "$TMPFILE"
echo "Build complete. Removed temporary token file."
