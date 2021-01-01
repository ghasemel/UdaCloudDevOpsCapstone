#!/usr/bin/env bash

## Complete the following steps to get Docker running locally
REPO="ghasemel/inventory:v1"

# Step 1:
# Build image and add a descriptive tag
docker build --tag $REPO .

# Step 2: 
# List docker images
docker images $REPO

# Step 3: 
# Run inventory app
docker run -it -p 8000:80/tcp --name inventory $REPO