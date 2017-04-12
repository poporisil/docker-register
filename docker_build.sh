#!/usr/bin/env bash

RELEASE_VERSION=$(git describe --tags $(git rev-list --tags --max-count=1))
echo RELEASE_VERSION=${RELEASE_VERSION}

echo "# build docker-register image..."
docker build --rm=false -t poporisil/docker-register:${RELEASE_VERSION} .
