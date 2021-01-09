#!/usr/bin/env bash

## Complete the following steps to get Docker running locally
BUILD_MODE=$1

REPO="ghasemel/inventory:v1"
CONTAINER_NAME="inventory$(date +"%y%m%d-%H%M%S")"

# Step 1:
# Build image and add a descriptive tag
docker build --tag $REPO .
echo $?

if [[ $? != 0 ]]; then
  exit 1
fi

# Step 2: 
# List docker images
docker images $REPO

# Step 3: 
# Run inventory app
if [ "$BUILD_MODE" = "build" ]; then
  docker run -d -p 8000:80/tcp --name "$CONTAINER_NAME" $REPO
  docker ps | grep "$CONTAINER_NAME"
  docker stop "$CONTAINER_NAME"
  docker rm "$CONTAINER_NAME"
else
  docker run -it -p 8000:80/tcp --name "$CONTAINER_NAME" $REPO
fi