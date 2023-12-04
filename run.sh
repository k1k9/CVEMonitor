#!/bin/bash
set -e

ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Remove old html directory
if [ -d "$ROOTDIR/html" ]; then
    rm -rf "$ROOTDIR/html" || { echo "Error removing html directory"; exit 1; }
    echo "Removed html directory"
fi

# Remove old backend container
docker compose -f "$ROOTDIR/docker-compose.yml" down || { echo "Error stopping docker compose"; exit 1; }


# Rebuild frontend
cd "$ROOTDIR/frontend" || { echo "Error: Directory $ROOTDIR/frontend not found"; exit 1; }
echo "VITE_BACKEND_URL: '$BACKEND_URL'" > ./.env
npm install || { echo "Error running npm install"; exit 1; }
npm run build || { echo "Error running npm run build"; exit 1; }
mv "$ROOTDIR/frontend/dist" "$ROOTDIR/html" || { echo "Error moving frontend/dist to html"; exit 1; }
cd "$ROOTDIR" || { echo "Error: Directory $ROOTDIR not found"; exit 1; }
echo "Rebuilt frontend"

# Run backend
docker compose -f "$ROOTDIR/docker-compose.yml" up -d || { echo "Error running docker compose"; exit 1; }

echo "Please restart your nginx"