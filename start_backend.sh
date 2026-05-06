#!/bin/bash

echo "Démarrage du backend Renote..."

if docker ps --format '{{.Names}}' | grep -q "^renote$"; then
    echo "✅ Backend déjà en cours (http://localhost:8000)"
elif docker ps -a --format '{{.Names}}' | grep -q "^renote$"; then
    docker start renote
    echo "✅ Backend lancé sur http://localhost:8000"
else
    docker run -d -p 8000:8000 --name renote renote-app
    echo "✅ Backend lancé sur http://localhost:8000"
fi
