"""
test_api.py — Tests des endpoints REST de l'API Renote.

Usage :
    python3 test_api.py

Prérequis :
    - L'app tourne sur http://localhost:8000
    - Être connecté dans le navigateur sur localhost:8000
    - Copier les cookies depuis DevTools (F12 → Application → Cookies) :
        renote_session  → SESSION ci-dessous
        XSRF-TOKEN      → XSRF ci-dessous
"""

import json
import urllib.parse
import urllib.request

# ── Collez vos cookies ici ───────────────────────────────────────────────────
SESSION = "eyJpdiI6Imt0bWdZZnRrR2hMRVZKakpBRzJoQkE9PSIsInZhbHVlIjoieVVZeXBIQWs0bC9udGo0ZEtkbm44S3ViZXY3Mktqc1lXeGFJcHpESTZneG9TVW1SYUErK054RUVJd0xVT1dFQzZacExYMkRFVkxLMXZoRU1GT0F0aVZyNlh0bUhwdG1kVGJ2YnNjTis4aFlDaEFNQWtFdzZLYkx1ODVZZ3JDd2QiLCJtYWMiOiI3ZGE2NjJlZWYwMmJiYzNmZmExNTE3M2IzNWRmOWM5ZmUzOTM4NTljMWIzYTNkNGVkMGUyOTEyMDVkOWQzYTlhIiwidGFnIjoiIn0%3D"
XSRF    = "eyJpdiI6InB2SWROc1pIdzE1bU5wOHU4d2Yydnc9PSIsInZhbHVlIjoiM0h2blYxY2tTU1I4OXgxYVBCNVA1TS85MDVSWlpGL3FpbE9HaGxERGt6ZWRUVVBtcmd4c3hiS2pRWGJXQTFjUWk2aWtvMWFGMm5HODdpcVB4b0V6U1hUWEdqdXZLUUxSZ3pzV053dFEwUTVVK0Z4QTNVS1ZNejczSkQ0MUdJcm4iLCJtYWMiOiI4MmRkYmQ2OTE0ZDEzNDQ1MzNmMjIwZjMxYzZlNTJlYTk3NDcyYTYwMTA2OTI3ZGQ1NjVmNTEyOGYzYjZjNjQ2IiwidGFnIjoiIn0%3D"
# ─────────────────────────────────────────────────────────────────────────────

BASE = "http://localhost:8000"

# Décode le XSRF token pour le header (URL-encoded → string)
XSRF_DECODED = urllib.parse.unquote(XSRF)

RESULTS = []


def call(method: str, path: str, body: dict = None) -> tuple[int, dict]:
    """Envoie une requête HTTP authentifiée et retourne (status_code, json_body)."""
    url = BASE + path
    data = json.dumps(body).encode() if body else None

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept",       "application/json")
    req.add_header("Content-Type", "application/json")
    req.add_header("Cookie",       f"renote_session={SESSION}; XSRF-TOKEN={XSRF}")
    req.add_header("X-XSRF-TOKEN", XSRF_DECODED)

    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test(label: str, method: str, path: str, body: dict, expected_code: int):
    """Lance un test et affiche le résultat."""
    code, resp = call(method, path, body)
    ok = code == expected_code
    icon = "✅" if ok else "❌"
    RESULTS.append((label, ok))

    print(f"\n{icon}  {label}")
    print(f"   {method} {path} → HTTP {code} (attendu {expected_code})")
    print("   " + json.dumps(resp, ensure_ascii=False, indent=3).replace("\n", "\n   "))


# ── Tests ────────────────────────────────────────────────────────────────────

print("━" * 45)
print("  Renote API — Tests automatisés")
print("━" * 45)

print("\n─── TAGS ───")

test("GET tous les tags",              "GET",  "/api/tags", None,              200)
test("POST créer un tag",              "POST", "/api/tags", {"name": "Tag Python"}, 201)
test("POST tag dupliqué (422 attendu)","POST", "/api/tags", {"name": "Tag Python"}, 422)

print("\n─── NOTES ───")

# Récupère l'id du premier tag pour créer la note
_, tags_resp = call("GET", "/api/tags")
tag_id = tags_resp["data"][0]["id"]

test("POST créer une note",            "POST",   "/api/notes",
     {"text": "Note créée depuis Python", "tag_id": tag_id}, 201)

test("GET toutes les notes",           "GET",    "/api/notes", None, 200)

# Récupère l'id de la première note pour la supprimer
_, notes_resp = call("GET", "/api/notes")
note_id = notes_resp["data"][0]["id"]

test(f"DELETE note existante (id={note_id})", "DELETE", f"/api/notes/{note_id}", None, 200)
test("DELETE note inexistante (404 attendu)", "DELETE", "/api/notes/99999",      None, 404)

# ── Résumé ───────────────────────────────────────────────────────────────────

passed = sum(1 for _, ok in RESULTS if ok)
total  = len(RESULTS)

print("\n" + "━" * 45)
print(f"  Résultat : {passed}/{total} tests passés")
print("━" * 45)
