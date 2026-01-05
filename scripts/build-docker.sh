#!/bin/bash
set -e

IMAGE_NAME="sparsetagging"
VERSION="2.4.0"
TAG="${IMAGE_NAME}:${VERSION}"

echo "🐳 Building Docker image: ${TAG}"
docker build -t "${TAG}" -t "${IMAGE_NAME}:latest" .

echo ""
echo "🔍 Scanning image with Trivy..."
trivy image --severity HIGH,CRITICAL "${TAG}"

echo ""
echo "📋 Generating SBOM..."
trivy image --format spdx-json --output sbom.json "${TAG}"

echo ""
echo "✅ Build and scan complete!"
echo "   Image: ${TAG}"
echo "   SBOM: sbom.json"
echo ""
echo "Run the image:"
echo "   docker run --rm ${TAG}"
echo ""
echo "Interactive shell:"
echo "   docker run --rm -it ${TAG} /bin/bash"
