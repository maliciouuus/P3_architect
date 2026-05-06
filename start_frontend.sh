#!/bin/bash

echo "Démarrage du frontend Renote..."
echo "➜ http://localhost:5174"
echo ""

cd "$(dirname "$0")/frontend" && npm run dev
