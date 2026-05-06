"""
test_api.py — Tests complets de l'API REST Renote.

Usage :
    python3 test_api.py

Prérequis :
    - Le backend tourne sur http://localhost:8000
    - Pas besoin du frontend, pas besoin de cookies
    - Auth via Bearer token (Sanctum)
"""

import json
import urllib.request
import urllib.error
import uuid

BASE    = "http://localhost:8000"
TOKEN   = None   # Sera rempli après le login
RESULTS = []


def call(method: str, path: str, body: dict = None, token: str = None) -> tuple[int, dict]:
    """Envoie une requête HTTP et retourne (status_code, json_body)."""
    url  = BASE + path
    data = json.dumps(body).encode() if body else None

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept",       "application/json")
    req.add_header("Content-Type", "application/json")

    # Auth Bearer token — utilisé pour toutes les routes protégées
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test(label: str, method: str, path: str, body: dict, expected_code: int, token: str = None):
    """Lance un test, affiche le résultat et retourne la réponse."""
    code, resp = call(method, path, body, token)
    ok   = code == expected_code
    icon = "✅" if ok else "❌"
    RESULTS.append((label, ok))

    print(f"\n{icon}  {label}")
    print(f"   {method} {path} → HTTP {code} (attendu {expected_code})")
    print("   " + json.dumps(resp, ensure_ascii=False, indent=3).replace("\n", "\n   "))
    return resp


# ─────────────────────────────────────────────────────────────────────────────
print("━" * 50)
print("  Renote API — Tests automatisés")
print("━" * 50)

# Identifiants uniques pour éviter les conflits entre les runs
uid   = uuid.uuid4().hex[:6]
email = f"test_{uid}@renote.fr"
tag1  = f"Travail_{uid}"
tag2  = f"Personnel_{uid}"

# ─── AUTH ─────────────────────────────────────────────────────────────────────
print("\n─── AUTH ───")

# Register
resp = test(
    "POST /api/register — créer un compte",
    "POST", "/api/register",
    {"name": "Test User", "email": email, "password": "password123"},
    201
)
register_token = resp.get("token")

# Login avec mauvais mot de passe (401 attendu)
test(
    "POST /api/login — mauvais mot de passe (401 attendu)",
    "POST", "/api/login",
    {"email": email, "password": "mauvais_mdp"},
    401
)

# Login correct — récupère le token pour la suite
resp = test(
    "POST /api/login — connexion réussie",
    "POST", "/api/login",
    {"email": email, "password": "password123"},
    200
)
TOKEN = resp.get("token")

# Appel protégé sans token (401 attendu)
test(
    "GET /api/notes sans token (401 attendu)",
    "GET", "/api/notes",
    None,
    401
)

# ─── TAGS ─────────────────────────────────────────────────────────────────────
print("\n─── TAGS ───")

test(
    "GET /api/tags — liste vide au départ",
    "GET", "/api/tags",
    None, 200, TOKEN
)

resp = test(
    f"POST /api/tags — créer '{tag1}'",
    "POST", "/api/tags",
    {"name": tag1},
    201, TOKEN
)
tag_id = resp.get("data", {}).get("id")

test(
    f"POST /api/tags — créer '{tag2}'",
    "POST", "/api/tags",
    {"name": tag2},
    201, TOKEN
)

test(
    "POST /api/tags — nom dupliqué (422 attendu)",
    "POST", "/api/tags",
    {"name": tag1},
    422, TOKEN
)

test(
    "GET /api/tags — liste avec 2 tags",
    "GET", "/api/tags",
    None, 200, TOKEN
)

# ─── NOTES ────────────────────────────────────────────────────────────────────
print("\n─── NOTES ───")

test(
    "POST /api/notes — champs manquants (422 attendu)",
    "POST", "/api/notes",
    {"text": "Note sans tag"},
    422, TOKEN
)

resp = test(
    "POST /api/notes — créer une note",
    "POST", "/api/notes",
    {"text": "Ma première note via API", "tag_id": tag_id},
    201, TOKEN
)
note_id = resp.get("data", {}).get("id")

resp = test(
    "POST /api/notes — créer une deuxième note",
    "POST", "/api/notes",
    {"text": "Deuxième note de test", "tag_id": tag_id},
    201, TOKEN
)
note_id_2 = resp.get("data", {}).get("id")

test(
    "GET /api/notes — liste avec 2 notes",
    "GET", "/api/notes",
    None, 200, TOKEN
)

test(
    f"DELETE /api/notes/{note_id} — supprimer la première note",
    "DELETE", f"/api/notes/{note_id}",
    None, 200, TOKEN
)

test(
    "DELETE /api/notes/99999 — note inexistante (404 attendu)",
    "DELETE", "/api/notes/99999",
    None, 404, TOKEN
)

test(
    "GET /api/notes — plus qu'une note",
    "GET", "/api/notes",
    None, 200, TOKEN
)

# ─── LOGOUT ───────────────────────────────────────────────────────────────────
print("\n─── LOGOUT ───")

test(
    "POST /api/logout — déconnexion",
    "POST", "/api/logout",
    None, 200, TOKEN
)

test(
    "GET /api/notes après logout (401 attendu)",
    "GET", "/api/notes",
    None, 401, TOKEN
)

# ─── Résumé ───────────────────────────────────────────────────────────────────
passed = sum(1 for _, ok in RESULTS if ok)
total  = len(RESULTS)

print("\n" + "━" * 50)
print(f"  Résultat : {passed}/{total} tests passés")
if passed < total:
    print("\n  Tests échoués :")
    for label, ok in RESULTS:
        if not ok:
            print(f"  ❌  {label}")
print("━" * 50)
