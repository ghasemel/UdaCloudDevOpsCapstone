#!/usr/bin/env bash
# This file tags and uploads an image to Docker Hub

# Assumes that an image is built via `run_docker.sh`

# Step 1:
# Create dockerpath
# dockerpath=<your docker ID/path>
dockerpath="ghasemel/inventory:v1"

# Step 2:  
# Authenticate & tag
echo "Docker ID and Image: $dockerpath"
if [ -z "$DOCKER_REPO_TOKEN" ]; then
  docker login --username ghasemel
else
  echo "$DOCKER_REPO_TOKEN" | docker login --username ghasemel --password-stdin
fi

# Step 3:
# Push image to a docker repository
docker push $dockerpath
