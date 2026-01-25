#!/bin/bash
set -e

# Build binaries
./scripts/build-release.sh

# Build zip for winget
./scripts/build-win-zip.sh

# Generate winget manifest
./scripts/generate-winget.sh

# Build deb
./scripts/build-deb.sh

echo "All packages built successfully!"
