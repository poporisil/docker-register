#!/usr/bin/env bash

RELEASE_VERSION=$(git describe --tags $(git rev-list --tags --max-count=1))
echo RELEASE_VERSION=${RELEASE_VERSION}

echo "# push docker-register image..."
docker push poporisil/docker-register:${RELEASE_VERSION}
docker tag poporisil/docker-register:${RELEASE_VERSION} poporisil/docker-register:latest
docker push poporisil/docker-register:latest
