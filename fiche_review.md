# Fiche de révision — Review P3 Renote

---

## 1. Les principes SOLID — à connaître par cœur

### S — Single Responsibility
**Définition :** Une classe = une seule raison de changer.
**Dans Renote :**
- `NoteController` → gère uniquement HTTP (reçoit, valide, répond)
- `NoteService` → contient uniquement la logique métier des notes
- `Note` (Model) → accède uniquement à la BDD

**Question piège :** *"Pourquoi ne pas tout mettre dans le Controller ?"*
→ Si la logique de création change ET que le format JSON change, on touche au même fichier = violation de S.

---

### O — Open/Closed
**Définition :** Ouvert à l'extension, fermé à la modification.
**Dans Renote :**
→ Ajouter un endpoint `PUT /api/notes/{id}` ne nécessite pas de modifier les endpoints existants. On ajoute une méthode `update()` dans le controller sans toucher à `index()`, `store()`, `destroy()`.

---

### L — Liskov Substitution
**Définition :** Une sous-classe doit pouvoir remplacer sa classe parente sans casser le programme.
**Dans Renote :**
→ Peu applicable ici. `NoteController extends Controller` sans surcharger de comportements critiques.
→ Si le mentor pose la question : *"C'est le principe le moins visible dans ce projet, mais il est respecté."*

---

### I — Interface Segregation
**Définition :** Ne pas forcer une classe à implémenter ce dont elle n'a pas besoin.
**Dans Renote :**
→ `NoteController` n'expose que les routes notes.
→ `TagController` n'expose que les routes tags.
→ Pas de contrôleur "fourre-tout" qui mélange les deux.

---

### D — Dependency Inversion
**Définition :** Dépendre des abstractions, pas des implémentations concrètes.
**Dans Renote :**
```php
// ❌ Sans injection
$service = new NoteService(); // couplage fort

// ✅ Avec injection
public function __construct(private NoteService $noteService) {}
// Laravel crée et injecte NoteService automatiquement
```
**Pourquoi c'est important :**
- Testable : on peut passer un faux NoteService dans les tests
- Flexible : changer NoteService ne touche pas au Controller

---

## 2. Le pattern MVC

**M — Model** (`app/Models/`) → parle à la BDD via Eloquent ORM
**V — View** (`resources/js/components/`) → affiche les données (React)
**C — Controller** (`app/Http/Controllers/Api/`) → fait le lien HTTP

**Ce qu'on a ajouté : la couche Service**
→ MVC pur : Controller parle directement au Model
→ Notre architecture : Controller → Service → Model
→ Pourquoi ? Parce que la logique métier dans le Controller viole le S de SOLID.

---

## 3. L'API REST — conventions à connaître

| Verbe | Action | Dans Renote |
|---|---|---|
| GET | Lecture | GET /api/notes → liste les notes |
| POST | Création | POST /api/notes → crée une note |
| DELETE | Suppression | DELETE /api/notes/{id} → supprime |

**Codes HTTP :**
- `200` → succès (GET, DELETE)
- `201` → ressource créée (POST)
- `401` → non authentifié
- `404` → ressource introuvable
- `422` → validation échouée (champ manquant, nom dupliqué)

**Format de réponse uniforme :**
```json
{ "status": "success", "data": {...}, "message": "..." }
```

---

## 4. Zustand et le state management

**Pourquoi un state manager ?**
→ `NoteForm` crée une note → `NoteList` doit l'afficher
→ Sans store : impossible de partager l'état entre composants non liés
→ Avec Zustand : les deux lisent le même store, tout se synchronise automatiquement

**Pattern utilisé : Flux**
```
Action → Store → UI
addNote() → set({notes}) → NoteList se re-rend
```

**Pourquoi Zustand plutôt que Redux ?**
→ Même concept mais 10x moins de code. Redux c'est trop lourd pour ce projet.

**Question piège :** *"C'est quoi la différence entre état local et état global ?"*
→ `text` et `tagId` dans NoteForm sont **locaux** (juste pour le formulaire, pas partagés)
→ `notes` et `tags` dans le store sont **globaux** (partagés entre NoteForm, NoteList, TagForm)

---

## 5. L'architecture globale — le fil rouge

```
AVANT (server-driven)          APRÈS (client-driven)
─────────────────────          ─────────────────────
Navigateur                     React (navigateur)
    ↕ HTML                         ↕ JSON
Livewire (PHP)                 API REST (Laravel)
    ↕ SQL                          ↕ Eloquent
SQLite                         SQLite
```

**Pourquoi cette migration ?**
→ Livewire génère le HTML côté serveur → impossible d'avoir une app mobile
→ React + API → le même back-end peut servir web, mobile, services externes

---

## 6. Questions probables du mentor

**Q : Qu'est-ce que SOLID ?**
→ 5 principes de conception orientée objet pour écrire du code maintenable, testable et évolutif.

**Q : Expliquez le S de SOLID dans votre projet.**
→ NoteController gère HTTP, NoteService gère la logique métier, Note gère la BDD. Chacun a une seule responsabilité.

**Q : Pourquoi avez-vous choisi Zustand ?**
→ Simple, léger, pas de boilerplate. Même concept que Redux (pattern Flux) mais adapté à la taille du projet.

**Q : Comment fonctionne l'injection de dépendances dans Laravel ?**
→ Le Controller déclare NoteService dans son constructeur. Laravel le crée et l'injecte automatiquement. Le Controller ne fait jamais `new NoteService()`.

**Q : Qu'est-ce qu'une architecture server-driven vs client-driven ?**
→ Server-driven : le HTML est généré par le serveur (Livewire). Client-driven : le serveur envoie du JSON, le client (React) génère le HTML.

**Q : Pourquoi séparer le front du back ?**
→ Pour que le même back-end puisse être consommé par plusieurs clients (web, mobile). Et pour déployer front et back indépendamment.

**Q : C'est quoi le pattern Observer et son lien avec MVC ?**
→ Observer : un objet notifie ses abonnés quand il change. Dans MVC, le Model est l'Observable, la View est l'Observer. Dans notre projet, le store Zustand joue ce rôle.

---

## 7. Les fichiers clés à relire

1. `routes/api.php` → les 5 endpoints
2. `app/Services/NoteService.php` → principe S
3. `app/Http/Controllers/Api/NoteController.php` → principe D
4. `resources/js/store/useAppStore.js` → Zustand + pattern Flux
5. `resources/js/services/api.js` → découplage axios

---

## 8. Ce que vous pouvez dire si vous ne savez pas

- *"Dans ce projet je n'ai pas eu à l'implémenter mais je sais que..."*
- *"J'ai fait le choix de X plutôt que Y parce que pour ce projet..."*
- *"C'est quelque chose que j'approfondirais en production en ajoutant..."*

**Ne jamais dire :** "Je ne sais pas" sans enchaîner avec quelque chose.
