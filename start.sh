#!/bin/bash

echo "Démarrage de Renote..."

# Si le container tourne déjà
if docker ps --format '{{.Names}}' | grep -q "^renote$"; then
    echo "✅ Renote tourne déjà sur http://localhost:8000"

# Si le container existe mais est arrêté
elif docker ps -a --format '{{.Names}}' | grep -q "^renote$"; then
    docker start renote
    echo "✅ Renote tourne sur http://localhost:8000"

# Sinon on le recrée depuis l'image
else
    docker run -d -p 8000:8000 --name renote renote-app
    echo "✅ Renote tourne sur http://localhost:8000"
fi

echo "   Login : test@renote.fr / password123"
