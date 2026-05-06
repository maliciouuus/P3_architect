from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

W, H = A4
doc = SimpleDocTemplate(
    "/home/sacha/Public/openclassroom/architect/P3_architect/documentation_architecture_renote.pdf",
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

BLUE   = colors.HexColor("#1a56db")
LBLUE  = colors.HexColor("#e8f0fe")
DGRAY  = colors.HexColor("#1f2937")
MGRAY  = colors.HexColor("#6b7280")
LGRAY  = colors.HexColor("#f3f4f6")
GREEN  = colors.HexColor("#065f46")
LGREEN = colors.HexColor("#d1fae5")
RED    = colors.HexColor("#991b1b")
LRED   = colors.HexColor("#fee2e2")
ORANGE = colors.HexColor("#92400e")
LORANGE= colors.HexColor("#fef3c7")
WHITE  = colors.white
BLACK  = colors.black

styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_s  = S("ts",  fontSize=26, textColor=BLUE,  spaceAfter=4,  spaceBefore=6,  leading=32, fontName="Helvetica-Bold", alignment=TA_CENTER)
sub_s    = S("ss",  fontSize=13, textColor=MGRAY, spaceAfter=10, leading=18, alignment=TA_CENTER)
h1_s     = S("h1s", fontSize=17, textColor=WHITE, spaceAfter=4,  spaceBefore=14, leading=22, fontName="Helvetica-Bold")
h2_s     = S("h2s", fontSize=13, textColor=BLUE,  spaceAfter=3,  spaceBefore=10, leading=17, fontName="Helvetica-Bold")
h3_s     = S("h3s", fontSize=11, textColor=DGRAY, spaceAfter=2,  spaceBefore=6,  leading=15, fontName="Helvetica-Bold")
body_s   = S("bs",  fontSize=10, textColor=DGRAY, spaceAfter=4,  leading=15, alignment=TA_JUSTIFY)
code_s   = S("cs",  fontSize=8.5,textColor=colors.HexColor("#c7254e"), spaceAfter=4, leading=13,
             fontName="Courier", backColor=colors.HexColor("#f9f9f9"),
             leftIndent=10, rightIndent=10, borderPadding=6)
bullet_s = S("bls", fontSize=10, textColor=DGRAY, spaceAfter=2,  leading=15, leftIndent=14, bulletIndent=4)
cap_s    = S("cap", fontSize=8,  textColor=MGRAY, spaceAfter=6,  leading=11, alignment=TA_CENTER)
label_s  = S("lbs", fontSize=9,  textColor=WHITE, leading=13, fontName="Helvetica-Bold")
cell_s   = S("cels",fontSize=9,  textColor=DGRAY, leading=13)
cell_h_s = S("chs", fontSize=9,  textColor=WHITE, leading=13, fontName="Helvetica-Bold")
note_s   = S("ns",  fontSize=9,  textColor=ORANGE,spaceAfter=4,  leading=13,
             backColor=LORANGE, leftIndent=8, rightIndent=8, borderPadding=5)

def HR(color=BLUE, thick=1):
    return HRFlowable(width="100%", thickness=thick, color=color, spaceAfter=6, spaceBefore=3)

def sp(n=8): return Spacer(1, n)

def h1(text):
    bg = Table([[Paragraph(text, h1_s)]], colWidths=[17*cm])
    bg.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    return bg

def h2(text): return Paragraph(text, h2_s)
def h3(text): return Paragraph(text, h3_s)
def body(text): return Paragraph(text, body_s)
def bullet(text, indent=0):
    st = ParagraphStyle("bx", parent=bullet_s, leftIndent=14+indent*12)
    return Paragraph("•  " + text, st)
def code(text):
    return Paragraph(text.replace("\n","<br/>").replace(" ","&nbsp;"), code_s)
def note(text): return Paragraph("ℹ  " + text, note_s)

def wrap_cells(data, first_row_bold=True):
    result = []
    for r, row in enumerate(data):
        new_row = []
        for cell in row:
            if isinstance(cell, str):
                st = cell_h_s if (r == 0 and first_row_bold) else cell_s
                new_row.append(Paragraph(cell, st))
            else:
                new_row.append(cell)
        result.append(new_row)
    return result

def table(data, col_widths, row_bgs=None, header_bg=BLUE):
    row_bgs = row_bgs or [LGRAY, WHITE]
    t = Table(wrap_cells(data), colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  header_bg),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), row_bgs),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t

def arch_box(label, sublabel, color):
    inner = Table([[Paragraph(label, S("lb", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold", leading=14)),
                    Paragraph(sublabel, S("sl", fontSize=8.5, textColor=colors.HexColor("#e5e7eb"), leading=12))]],
                  colWidths=[6*cm, 10*cm])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return inner

story = []

# ═══════════════════════════════════════════════════════════════
# PAGE DE TITRE
# ═══════════════════════════════════════════════════════════════
story.append(Spacer(1, 4*cm))
story.append(Paragraph("Documentation d'Architecture", title_s))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Renote — Migration server-driven → client-driven", sub_s))
story.append(Spacer(1, 0.2*cm))
story.append(HR(BLUE, 2))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Projet P3 — OpenClassrooms", S("p3", fontSize=11, textColor=MGRAY, alignment=TA_CENTER)))
story.append(Paragraph("PHP 8.4 / Laravel 12  ·  React 18  ·  Zustand  ·  Sanctum  ·  SQLite", S("st", fontSize=10, textColor=MGRAY, alignment=TA_CENTER)))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 1 — INTRODUCTION
# ═══════════════════════════════════════════════════════════════
story.append(h1("1. Introduction"))
story.append(sp())
story.append(body(
    "Renote est une application web de prise de notes permettant à un utilisateur de créer, "
    "visualiser et organiser ses notes à l'aide de tags. L'objectif de cette refonte est de "
    "faire évoluer l'application d'une architecture monolithique server-driven vers une "
    "architecture client-driven découplée, afin de supporter plusieurs interfaces clientes "
    "(web, mobile) et d'exposer une API REST consommable par des services externes."
))
story.append(sp(4))
story.append(body("Cette documentation décrit les quatre transformations réalisées :"))
story.append(sp(4))

transformations = [
    ("Migration server-driven → client-driven",
     "Le HTML n'est plus généré par PHP. React gère l'affichage côté navigateur. "
     "Le back-end PHP répond exclusivement en JSON."),
    ("Passage au pattern MVC",
     "Le code est réorganisé en Controllers (HTTP), Services (logique métier) "
     "et Models (accès données). Chaque couche a une responsabilité unique (principe S de SOLID)."),
    ("Découplage complet front / back",
     "Le backend (backend/) est une API PHP pure sans vues. "
     "Le frontend (frontend/) est une app React standalone avec Vite. "
     "Les deux communiquent exclusivement via l'API REST."),
    ("Authentification sans état via Sanctum",
     "Laravel Sanctum génère des tokens Bearer stockés en BDD (personal_access_tokens). "
     "Plus de cookies de session ni de CSRF — compatible Postman, mobile et web."),
    ("Ajout d'un state management côté front",
     "Zustand gère l'état global partagé entre composants React "
     "(notes, tags, token, loading, error) selon le pattern Flux."),
]
data = [["Transformation", "Description"]]
for t_title, t_desc in transformations:
    data.append([t_title, t_desc])
story.append(table(data, [5.5*cm, 11.5*cm]))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 2 — ARCHITECTURE DE BASE
# ═══════════════════════════════════════════════════════════════
story.append(h1("2. Architecture de base"))
story.append(sp())

story.append(h2("2.1 Diagramme de composants (architecture de base)"))
story.append(sp(4))
story.append(body(
    "L'architecture initiale est entièrement server-driven. "
    "Livewire génère le HTML côté serveur PHP et gère les interactions via WebSockets PHP. "
    "Il n'y a aucune séparation entre le front et le back."
))
story.append(sp(6))

# Diagramme architecture de base
diag_base = [
    (colors.HexColor("#1e3a5f"), "Navigateur",         "HTML rendu côté serveur — wire:* pour les interactions"),
    (colors.HexColor("#1e3a5f"), "⬇  HTTP (HTML)",     "Aller-retour serveur à chaque interaction"),
    (colors.HexColor("#7f1d1d"), "Composant Livewire",
     "Notes.php / TagForm.php\n— Validation  — Accès BDD  — État UI  — Messages flash\n"
     "⚠ 5 responsabilités dans une seule classe"),
    (colors.HexColor("#1e3a5f"), "⬇  Eloquent ORM",    ""),
    (colors.HexColor("#1a3a2a"), "Models Eloquent",     "Note.php  ·  Tag.php  ·  User.php"),
    (colors.HexColor("#1e3a5f"), "⬇  SQL",             ""),
    (colors.HexColor("#1a3a2a"), "Base de données",     "SQLite — database.sqlite"),
]
for bg, label, desc in diag_base:
    full = label if not desc else f"{label}   —   {desc}"
    is_warn = "⚠" in desc
    t = Table([[Paragraph(full, S("db", fontSize=9, textColor=WHITE if not is_warn else colors.HexColor("#fca5a5"),
                                  leading=13, fontName="Helvetica-Bold" if "⬇" not in label else "Helvetica"))]], colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#374151")),
    ]))
    story.append(t)
    story.append(sp(2))

story.append(sp(4))
story.append(Paragraph("⚠  En rouge : le composant Livewire qui cumule toutes les responsabilités.", cap_s))
story.append(sp(8))

story.append(h2("2.2 Points faibles constatés"))
story.append(sp(4))

weak_points = [
    ("Couplage fort",
     "Les composants Livewire (Notes.php, TagForm.php) mélangent validation, "
     "accès BDD, état UI et gestion des messages. Aucune séparation de responsabilités."),
    ("Absence d'API",
     "routes/web.php ne contient que des routes HTML. "
     "Aucun endpoint /api/* n'existe. Le front est indissociable du back."),
    ("Architecture non scalable",
     "Livewire génère le HTML côté serveur. Il est impossible d'avoir une app mobile "
     "ou un second client web sans refactorisation complète."),
    ("Duplication de logique",
     "Tag::all() est appelé dans mount() ET refreshTags() dans Notes.php — "
     "même requête dupliquée. Viole le principe DRY."),
    ("Testabilité nulle",
     "La logique métier est dans les composants Livewire. "
     "Il est impossible de tester create() ou delete() sans démarrer Laravel entier."),
]
data = [["Point faible", "Description"]]
for wp, desc in weak_points:
    data.append([wp, desc])
story.append(table(data, [4.5*cm, 12.5*cm]))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 3 — ARCHITECTURE CIBLE
# ═══════════════════════════════════════════════════════════════
story.append(h1("3. Architecture cible"))
story.append(sp())

# ── 3a. Composants ──────────────────────────────────────────────
story.append(h2("3.a Composants d'architecture"))
story.append(sp(4))
story.append(body(
    "L'architecture cible sépare complètement le front-end React du back-end PHP/Laravel. "
    "La communication entre les deux se fait exclusivement via l'API REST (HTTP/JSON). "
    "Côté back-end, le pattern MVC est appliqué avec une couche Service supplémentaire."
))
story.append(sp(6))

diag_cible = [
    (colors.HexColor("#1e3a5f"), "FRONT-END standalone (frontend/  — React + Zustand)",
     "Login · Register · Dashboard · NoteForm · NoteList · TagForm  ·  services/api.js"),
    (colors.HexColor("#374151"), "⬇  HTTP REST / JSON  (axios + Authorization: Bearer {token})",  ""),
    (colors.HexColor("#1a3a2a"), "routes/api.php  (backend/)",
     "8 endpoints REST  ·  Middleware auth:sanctum  ·  Préfixe /api"),
    (colors.HexColor("#374151"), "⬇  Laravel Router", ""),
    (colors.HexColor("#4c1d95"), "Controllers  (couche HTTP)",
     "NoteController.php  ·  TagController.php\nReçoit la requête, valide, délègue au Service, renvoie JSON"),
    (colors.HexColor("#374151"), "⬇  Injection de dépendances (principe D)", ""),
    (colors.HexColor("#7c3aed"), "Services  (couche métier)",
     "NoteService.php  ·  TagService.php\nLogique métier pure — réutilisable et testable indépendamment"),
    (colors.HexColor("#374151"), "⬇  Eloquent ORM", ""),
    (colors.HexColor("#1a3a2a"), "Models  (couche données)",
     "Note.php  ·  Tag.php  ·  User.php  ·  Relations belongsTo / hasMany"),
    (colors.HexColor("#374151"), "⬇  PDO / SQL", ""),
    (colors.HexColor("#1e3a5f"), "Base de données SQLite", "database/database.sqlite"),
]
for bg, label, desc in diag_cible:
    is_arrow = "⬇" in label
    full = label if not desc else f"{label}   —   {desc}"
    st = S("dc", fontSize=9 if not is_arrow else 8.5, textColor=WHITE,
           leading=14 if "\n" in str(desc) else 13,
           fontName="Helvetica" if is_arrow else "Helvetica-Bold")
    t = Table([[Paragraph(full, st)]], colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), 5 if not is_arrow else 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5 if not is_arrow else 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#374151")),
    ]))
    story.append(t)
    story.append(sp(2))

story.append(sp(6))
story.append(h3("Protocoles de communication"))
data = [
    ["Lien", "Protocole", "Format", "Détail"],
    ["React → API Laravel",    "HTTP REST",     "JSON",       "axios + header Authorization: Bearer {token}"],
    ["API → Controller",       "Laravel Router","PHP interne","Middleware auth:sanctum vérifie le token Sanctum"],
    ["Controller → Service",   "Injection DI",  "PHP interne","Laravel injecte le Service automatiquement"],
    ["Service → Model",        "Eloquent ORM",  "PHP interne","Note::create(), Note::where(), Tag::all()"],
    ["Model → BDD",            "PDO / SQL",     "SQLite",     "Fichier database/database.sqlite"],
]
story.append(table(data, [3.5*cm, 3*cm, 2.5*cm, 8*cm]))
story.append(PageBreak())

# ── 3b. Spécifications API REST ─────────────────────────────────
story.append(h2("3.b Spécifications API REST"))
story.append(sp(4))
story.append(body(
    "Tous les endpoints sont préfixés par /api. "
    "Les endpoints protégés nécessitent le header : Authorization: Bearer {token}. "
    "Format de réponse uniforme : { \"status\": \"success\"|\"error\", \"data\": ..., \"message\": ... }"
))
story.append(sp(6))

# ── Auth endpoints
story.append(h3("Endpoints — Authentification (publics)"))
story.append(sp(4))

endpoints_auth = [
    {
        "method": "POST", "url": "/api/register",
        "desc": "Crée un compte utilisateur et retourne un token Sanctum. Le token est stocké dans la table personal_access_tokens.",
        "request": '{\n  "name": "Mon Nom",\n  "email": "mon@email.fr",\n  "password": "password123"\n}',
        "response_ok": '{\n  "status": "success",\n  "token": "1|nJCMiV5betpU045g...",\n  "user": { "id": 1, "name": "Mon Nom", "email": "mon@email.fr" }\n}',
        "codes": "201 Created — 422 Email déjà utilisé / validation échouée",
    },
    {
        "method": "POST", "url": "/api/login",
        "desc": "Authentifie un utilisateur et retourne un nouveau token Sanctum. Les anciens tokens sont supprimés.",
        "request": '{\n  "email": "mon@email.fr",\n  "password": "password123"\n}',
        "response_ok": '{\n  "status": "success",\n  "token": "2|FVZYUcYfMzMw...",\n  "user": { "id": 1, "name": "Mon Nom", "email": "mon@email.fr" }\n}',
        "codes": "200 OK — 401 Identifiants invalides",
    },
    {
        "method": "POST", "url": "/api/logout",
        "desc": "Révoque le token actuel (le supprime de personal_access_tokens). Nécessite le Bearer token.",
        "request": "Aucun body. Header requis : Authorization: Bearer {token}",
        "response_ok": '{\n  "status": "success",\n  "message": "Déconnecté."\n}',
        "codes": "200 OK — 401 Non authentifié",
    },
]

for ep in endpoints_auth:
    method_color = {"GET": LGREEN, "POST": LBLUE, "DELETE": LRED}[ep["method"]]
    method_text_color = {"GET": GREEN, "POST": BLUE, "DELETE": RED}[ep["method"]]
    header = Table([
        [Paragraph(ep["method"], S(f"ma{ep['url']}", fontSize=11, textColor=method_text_color, fontName="Helvetica-Bold")),
         Paragraph(ep["url"], S(f"ua{ep['url']}", fontSize=11, textColor=DGRAY, fontName="Courier")),
         Paragraph(ep["codes"], S(f"ca{ep['url']}", fontSize=9, textColor=MGRAY, leading=12))]
    ], colWidths=[2*cm, 5*cm, 10*cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), method_color),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ]))
    story.append(header)
    detail = Table([
        [Paragraph("Description", S(f"dla{ep['url']}", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["desc"], S(f"dva{ep['url']}", fontSize=9, textColor=DGRAY, leading=13))],
        [Paragraph("Requête", S(f"rqa{ep['url']}", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["request"].replace("\n","<br/>").replace(" ","&nbsp;"),
                   S(f"rva{ep['url']}", fontSize=8.5, textColor=colors.HexColor("#c7254e"), fontName="Courier", leading=12))],
        [Paragraph("Réponse JSON", S(f"rja{ep['url']}", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["response_ok"].replace("\n","<br/>").replace(" ","&nbsp;"),
                   S(f"roa{ep['url']}", fontSize=8.5, textColor=colors.HexColor("#c7254e"), fontName="Courier", leading=12))],
    ], colWidths=[2.5*cm, 14.5*cm])
    detail.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), LGRAY),
        ("BACKGROUND", (1,0), (1,-1), WHITE),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(detail)
    story.append(sp(8))

# ── Notes endpoints
story.append(h3("Endpoints — Notes (protégés — Bearer token requis)"))
story.append(sp(4))

endpoints_notes = [
    {
        "method": "GET", "url": "/api/notes",
        "desc": "Retourne toutes les notes de l'utilisateur connecté, avec leur tag associé (eager loading).",
        "request": "Aucun body. Header : Authorization: Bearer {token}",
        "response_ok": '{\n  "status": "success",\n  "data": [\n    {\n      "id": 1,\n      "text": "Ma note",\n      "tag": { "id": 2, "name": "Travail" },\n      "created_at": "2025-07-16T20:00:00.000000Z"\n    }\n  ]\n}',
        "codes": "200 OK — 401 Non authentifié",
    },
    {
        "method": "POST", "url": "/api/notes",
        "desc": "Crée une nouvelle note pour l'utilisateur connecté.",
        "request": '{\n  "text": "Contenu de la note",\n  "tag_id": 1\n}',
        "response_ok": '{\n  "status": "success",\n  "message": "Note créée.",\n  "data": {\n    "id": 5,\n    "text": "Contenu de la note",\n    "tag": { "id": 1, "name": "Personnel" },\n    "created_at": "..."\n  }\n}',
        "codes": "201 Created — 401 Non authentifié — 422 Validation échouée",
    },
    {
        "method": "DELETE", "url": "/api/notes/{id}",
        "desc": "Supprime une note. Vérifie que la note appartient à l'utilisateur connecté.",
        "request": "Aucun body. L'id est dans l'URL.",
        "response_ok": '{\n  "status": "success",\n  "message": "Note supprimée."\n}\n\n// Si la note n\'appartient pas à l\'user :\n{\n  "status": "error",\n  "message": "Note introuvable ou accès refusé."\n}',
        "codes": "200 OK — 401 Non authentifié — 404 Note introuvable/accès refusé",
    },
]

for ep in endpoints_notes:
    method_color = {"GET": LGREEN, "POST": LBLUE, "DELETE": LRED}[ep["method"]]
    method_text_color = {"GET": GREEN, "POST": BLUE, "DELETE": RED}[ep["method"]]

    header = Table([
        [Paragraph(ep["method"], S("m", fontSize=11, textColor=method_text_color, fontName="Helvetica-Bold")),
         Paragraph(ep["url"], S("u", fontSize=11, textColor=DGRAY, fontName="Courier")),
         Paragraph(ep["codes"], S("c", fontSize=9, textColor=MGRAY, leading=12))]
    ], colWidths=[2*cm, 5*cm, 10*cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), method_color),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ]))
    story.append(header)

    detail = Table([
        [Paragraph("Description", S("dl", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["desc"], S("dv", fontSize=9, textColor=DGRAY, leading=13))],
        [Paragraph("Requête", S("dl", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["request"].replace("\n","<br/>").replace(" ","&nbsp;"),
                   S("rv", fontSize=8.5, textColor=colors.HexColor("#c7254e"), fontName="Courier", leading=12))],
        [Paragraph("Réponse JSON", S("dl", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["response_ok"].replace("\n","<br/>").replace(" ","&nbsp;"),
                   S("rj", fontSize=8.5, textColor=colors.HexColor("#c7254e"), fontName="Courier", leading=12))],
    ], colWidths=[2.5*cm, 14.5*cm])
    detail.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), LGRAY),
        ("BACKGROUND", (1,0), (1,-1), WHITE),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(detail)
    story.append(sp(8))

story.append(h3("Endpoints — Tags (protégés — Bearer token requis)"))
story.append(sp(4))

endpoints_tags = [
    {
        "method": "GET", "url": "/api/tags",
        "desc": "Retourne la liste de tous les tags disponibles (non filtrés par utilisateur).",
        "request": "Aucun body. Header : Authorization: Bearer {token}",
        "response_ok": '{\n  "status": "success",\n  "data": [\n    { "id": 1, "name": "Personnel" },\n    { "id": 2, "name": "Travail" }\n  ]\n}',
        "codes": "200 OK — 401 Non authentifié",
    },
    {
        "method": "POST", "url": "/api/tags",
        "desc": "Crée un nouveau tag. Le nom doit être unique (max 50 caractères).",
        "request": '{\n  "name": "Travail"\n}',
        "response_ok": '{\n  "status": "success",\n  "message": "Tag créé.",\n  "data": { "id": 3, "name": "Travail" }\n}\n\n// Si le nom existe déjà :\n{\n  "status": "error",\n  "message": "The name has already been taken."\n}',
        "codes": "201 Created — 401 Non authentifié — 422 Validation (nom dupliqué ou trop long)",
    },
]

for ep in endpoints_tags:
    method_color = {"GET": LGREEN, "POST": LBLUE}[ep["method"]]
    method_text_color = {"GET": GREEN, "POST": BLUE}[ep["method"]]

    header = Table([
        [Paragraph(ep["method"], S("m2", fontSize=11, textColor=method_text_color, fontName="Helvetica-Bold")),
         Paragraph(ep["url"], S("u2", fontSize=11, textColor=DGRAY, fontName="Courier")),
         Paragraph(ep["codes"], S("c2", fontSize=9, textColor=MGRAY, leading=12))]
    ], colWidths=[2*cm, 5*cm, 10*cm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), method_color),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ]))
    story.append(header)

    detail = Table([
        [Paragraph("Description", S("dl2", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["desc"], S("dv2", fontSize=9, textColor=DGRAY, leading=13))],
        [Paragraph("Requête", S("dl3", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["request"].replace("\n","<br/>").replace(" ","&nbsp;"),
                   S("rv2", fontSize=8.5, textColor=colors.HexColor("#c7254e"), fontName="Courier", leading=12))],
        [Paragraph("Réponse JSON", S("dl4", fontSize=8.5, textColor=MGRAY, fontName="Helvetica-Bold")),
         Paragraph(ep["response_ok"].replace("\n","<br/>").replace(" ","&nbsp;"),
                   S("rj2", fontSize=8.5, textColor=colors.HexColor("#c7254e"), fontName="Courier", leading=12))],
    ], colWidths=[2.5*cm, 14.5*cm])
    detail.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), LGRAY),
        ("BACKGROUND", (1,0), (1,-1), WHITE),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(detail)
    story.append(sp(8))

story.append(PageBreak())

# ── 3c. Data flow state management ──────────────────────────────
story.append(h2("3.c Data flow du state management"))
story.append(sp(4))
story.append(body(
    "Zustand applique le pattern Flux : les actions modifient le store, "
    "les composants qui s'y abonnent se re-rendent automatiquement. "
    "Ci-dessous le flux complet pour la création d'une note."
))
story.append(sp(6))

story.append(h3("Flux actions / events → store → UI"))
story.append(sp(4))

flux = [
    ("EVENT",   "Utilisateur soumet le formulaire",
     "NoteForm.jsx — handleSubmit(e) déclenché par onSubmit du <form>"),
    ("ACTION",  "addNote(text, tag_id) appelée",
     "Le composant appelle addNote() du store Zustand — aucun appel fetch direct"),
    ("EFFET",   "Appel API POST /api/notes",
     "useAppStore : createNote(text, tag_id) → api.js → axios.post('/notes', {...})"),
    ("EFFET",   "Laravel traite la requête",
     "NoteController.store() → NoteService.create() → Note::create() → SQLite"),
    ("EFFET",   "Réponse JSON 201",
     '{ "status": "success", "data": { id, text, tag, created_at } }'),
    ("STORE",   "set({ notes: [newNote, ...state.notes] })",
     "Zustand met à jour l'état global — optimistic : on préfixe en tête de liste"),
    ("UI",      "NoteList.jsx se re-rend automatiquement",
     "Zustand notifie NoteList car il s'est abonné à state.notes via useAppStore(s => s.notes)"),
]

type_colors = {"EVENT": LBLUE, "ACTION": LORANGE, "EFFET": LGRAY, "STORE": LGREEN, "UI": colors.HexColor("#ede9fe")}
type_text   = {"EVENT": BLUE,  "ACTION": ORANGE,  "EFFET": MGRAY, "STORE": GREEN,  "UI": colors.HexColor("#5b21b6")}

data = [["Type", "Action", "Détail technique"]]
for typ, action, detail in flux:
    data.append([
        Paragraph(typ, S(f"t{typ}", fontSize=9, textColor=type_text[typ], fontName="Helvetica-Bold",
                         backColor=type_colors[typ], leading=13)),
        Paragraph(action, cell_s),
        Paragraph(detail, cell_s),
    ])
t = Table(wrap_cells(data), colWidths=[2*cm, 5.5*cm, 9.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), BLUE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LGRAY, WHITE]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(sp(8))

story.append(h3("Gestion des erreurs et état de chargement"))
story.append(sp(4))
story.append(body(
    "Le store Zustand centralise les états loading et error. "
    "Tout appel API commence par set({ loading: true, error: null }) "
    "et se termine soit par set({ loading: false }) en succès, "
    "soit par set({ error: message, loading: false }) en échec. "
    "Les composants lisent ces valeurs et affichent un spinner ou un message d'erreur."
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 4 — ANALYSE DE L'ÉCART
# ═══════════════════════════════════════════════════════════════
story.append(h1("4. Analyse de l'écart"))
story.append(sp())
story.append(body("Liste des composants ajoutés, modifiés et supprimés lors de la migration."))
story.append(sp(6))

story.append(h3("Composants ajoutés"))
story.append(sp(4))
added = [
    ["Fichier", "Type", "Rôle"],
    ["backend/app/Services/NoteService.php",              "Service PHP",      "Logique métier notes — getAllForUser(), create(), delete()"],
    ["backend/app/Services/TagService.php",               "Service PHP",      "Logique métier tags — getAll(), create()"],
    ["backend/app/Http/Controllers/Api/NoteController.php","Controller PHP",  "Gère les requêtes HTTP API notes (index, store, destroy)"],
    ["backend/app/Http/Controllers/Api/TagController.php","Controller PHP",   "Gère les requêtes HTTP API tags (index, store)"],
    ["backend/app/Http/Controllers/Api/AuthController.php","Controller PHP",  "Register, Login, Logout via Sanctum Bearer token"],
    ["backend/routes/api.php",                            "Routes Laravel",   "8 endpoints REST — auth publics + notes/tags protégés"],
    ["frontend/src/main.jsx",                             "Entrée React",     "Monte <App /> dans le div#root de index.html"],
    ["frontend/src/App.jsx",                              "Composant React",  "Routing Login/Register/Dashboard selon le token Zustand"],
    ["frontend/src/components/Login.jsx",                 "Composant React",  "Page connexion — appelle store.login()"],
    ["frontend/src/components/Register.jsx",              "Composant React",  "Page inscription — appelle store.register()"],
    ["frontend/src/components/Dashboard.jsx",             "Composant React",  "Page principale avec sidebar — charge les tags au montage"],
    ["frontend/src/components/NoteForm.jsx",              "Composant React",  "Formulaire création note — lit le store, appelle addNote()"],
    ["frontend/src/components/NoteList.jsx",              "Composant React",  "Liste notes — charge via fetchNotes(), appelle removeNote()"],
    ["frontend/src/components/TagForm.jsx",               "Composant React",  "Formulaire création tag — appelle addTag()"],
    ["frontend/src/store/useAppStore.js",                 "Store Zustand",    "État global (token, user, notes, tags, loading, error) + actions"],
    ["frontend/src/services/api.js",                      "Service JS",       "Couche API — Bearer token auto via intercepteur axios"],
]
t = Table(wrap_cells(added), colWidths=[6.5*cm, 2.8*cm, 7.7*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), GREEN),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LGREEN, WHITE]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(sp(10))

story.append(h3("Composants modifiés"))
story.append(sp(4))
modified = [
    ["Fichier", "Modification"],
    ["backend/bootstrap/app.php",
     "Ajout de api: routes/api.php dans withRouting() — suppression des middlewares de session web"],
    ["backend/composer.json",
     "Ajout de laravel/sanctum — suppression de livewire/flux et livewire/volt"],
    ["backend/app/Models/User.php",
     "Ajout du trait HasApiTokens (Sanctum) pour createToken() et tokens()"],
    ["backend/bootstrap/providers.php",
     "Suppression de VoltServiceProvider (Livewire supprimé)"],
    ["frontend/package.json",
     "Ajout de react, react-dom, zustand, axios, tailwindcss, @vitejs/plugin-react"],
    ["frontend/vite.config.js",
     "Configuration Vite standalone avec proxy /api → localhost:8000 pour éviter le CORS"],
]
t = Table(wrap_cells(modified), colWidths=[5.5*cm, 11.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#92400e")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LORANGE, WHITE]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(sp(10))

story.append(h3("Composants supprimés"))
story.append(sp(4))
deleted = [
    ["Fichier supprimé", "Remplacé par"],
    ["app/Livewire/Notes.php",
     "NoteController.php + NoteService.php + NoteList.jsx + NoteForm.jsx"],
    ["app/Livewire/TagForm.php",
     "TagController.php + TagService.php + TagForm.jsx"],
    ["app/Livewire/Actions/Logout.php",
     "AuthController.php → POST /api/logout"],
    ["resources/views/ (toutes les vues Blade)",
     "Composants React dans frontend/src/components/"],
    ["routes/web.php + routes/auth.php",
     "routes/api.php uniquement — le backend est une API pure sans HTML"],
    ["livewire/flux + livewire/volt (packages)",
     "laravel/sanctum pour l'authentification par token Bearer"],
]
t = Table(wrap_cells(deleted), colWidths=[7*cm, 10*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), RED),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LRED, WHITE]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d1d5db")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SECTION 5 — JUSTIFICATION DE L'APPROCHE
# ═══════════════════════════════════════════════════════════════
story.append(h1("5. Justification de l'approche architecturale"))
story.append(sp())

story.append(h2("5.1 Choix de Zustand pour le state management"))
story.append(sp(4))
story.append(body(
    "Zustand a été choisi pour sa simplicité et son faible volume de code. "
    "Redux Toolkit aurait été une alternative valide mais impose des conventions plus lourdes "
    "(slices, reducers, dispatch) inadaptées à un projet de cette taille. "
    "MobX aurait introduit le pattern MVVM avec des observables automatiques, "
    "mais sa courbe d'apprentissage est plus élevée. "
    "Le Context API natif React aurait causé des re-renders excessifs."
))
story.append(sp(4))
story.append(body(
    "Zustand implémente le pattern Flux de manière simplifiée : "
    "les actions (addNote, removeNote, addTag) modifient directement le store via set(). "
    "Les composants s'abonnent avec des sélecteurs ciblés (useAppStore(s => s.notes)) "
    "et ne se re-rendent que lorsque leur portion de l'état change."
))
story.append(sp(8))

story.append(h2("5.2 Principes SOLID appliqués"))
story.append(sp(4))

solid_table = [
    ["Principe", "Application dans Renote"],
    ["S — Single Responsibility",
     "Chaque classe a une seule responsabilité : NoteController gère HTTP, "
     "NoteService contient la logique métier, Note (Model) accède à la BDD. "
     "Côté React, chaque composant gère une seule partie de l'UI."],
    ["O — Open/Closed",
     "Ajouter un nouvel endpoint (ex. PUT /api/notes/{id}) ne nécessite pas de "
     "modifier NoteService ou les autres contrôleurs — on ajoute une méthode."],
    ["L — Liskov Substitution",
     "NoteController extends Controller sans surcharger de comportements critiques. "
     "Non directement observable ici faute d'héritage métier complexe."],
    ["I — Interface Segregation",
     "NoteController n'expose que les routes liées aux notes. "
     "TagController n'expose que les routes tags. Aucun contrôleur 'fourre-tout'."],
    ["D — Dependency Inversion",
     "NoteController ne fait pas new NoteService(). Il déclare sa dépendance "
     "dans le constructeur et Laravel l'injecte automatiquement. "
     "Côté React, les composants dépendent de api.js (abstraction), pas de fetch directement."],
]
story.append(table(solid_table, [3.5*cm, 13.5*cm]))
story.append(sp(8))

story.append(h2("5.3 Autres décisions techniques"))
story.append(sp(4))

decisions = [
    ("Séparation des responsabilités (SoC)",
     "La validation est faite dans le Controller (frontière système), "
     "pas dans le Service. Le Service est ainsi réutilisable sans valider deux fois."),
    ("Sanctum Bearer token pour l'authentification",
     "Sanctum génère des tokens opaques stockés en BDD (personal_access_tokens). "
     "Le token est retourné dans la réponse JSON après login/register. "
     "React le stocke en mémoire (Zustand) + localStorage et l'envoie via Authorization: Bearer. "
     "Compatible Postman, mobile et tout client HTTP — aucun cookie ni CSRF requis."),
    ("Séparation backend/ et frontend/ dans le repo",
     "Le backend est une API PHP pure (aucune vue, aucun asset front). "
     "Le frontend est une app React standalone avec Vite sur port 5174. "
     "Les deux peuvent être déployés indépendamment sur des serveurs différents."),
    ("SQLite comme base de données",
     "Base embarquée, zéro configuration. Facilement remplaçable par MySQL/PostgreSQL "
     "en changeant DB_CONNECTION dans .env — Laravel Eloquent abstrait le moteur SQL."),
    ("Format de réponse JSON uniforme",
     "{ status, data, message } pour toutes les réponses. "
     "Facilite la gestion côté React : on sait toujours où chercher les données."),
    ("Optimistic update dans le store",
     "Après création/suppression, on met à jour le store local sans re-fetcher toute la liste. "
     "Cela évite un aller-retour réseau inutile et rend l'UI plus réactive."),
]
data = [["Décision", "Justification"]]
for dec, justif in decisions:
    data.append([dec, justif])
story.append(table(data, [5*cm, 12*cm]))
story.append(sp(12))

story.append(HR(MGRAY))
story.append(Paragraph(
    "Documentation d'architecture — Projet P3 OpenClassrooms — PHP 8.4 / Laravel 12 / React 18 / Zustand / Sanctum",
    cap_s
))

doc.build(story)
print("PDF généré : documentation_architecture_renote.pdf")
